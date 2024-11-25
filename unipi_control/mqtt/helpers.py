"""Modbus helper to connect, subcribe and publish to MQTT."""

import asyncio
import time
import uuid
from asyncio import Task
from typing import Awaitable
from typing import Callable
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Set

from aiomqtt import MqttError

from unipi_control.config import Config
from unipi_control.config import LogPrefix
from unipi_control.config import UNIPI_LOGGER
from unipi_control.features.eastron import Eastron
from unipi_control.features.unipi import DigitalInput
from unipi_control.features.unipi import DigitalOutput
from unipi_control.features.unipi import Led
from unipi_control.features.unipi import Relay
from unipi_control.features.constants import FeatureType
from unipi_control.helpers.exceptions import UnexpectedError
from unipi_control.helpers.log import LOG_LEVEL
from unipi_control.helpers.log import LOG_MQTT_PUBLISH
from unipi_control.helpers.log import LOG_MQTT_SUBSCRIBE
from unipi_control.helpers.text import slugify
from unipi_control.integrations.covers import CoverMap
from unipi_control.mqtt.discovery.binary_sensors import HassBinarySensorsDiscovery
from unipi_control.mqtt.discovery.covers import HassCoversDiscovery
from unipi_control.mqtt.discovery.sensors import HassSensorsDiscovery
from unipi_control.mqtt.discovery.switches import HassSwitchesDiscovery
from unipi_control.hardware.unipi import Unipi

from aiomqtt import Client as MqttClient

from unipi_control.mqtt.integrations.covers import CoversMqttHelper


class MqttHelper:
    MQTT_RUNNING: ClassVar[bool] = True
    RETRY_RECONNECT: ClassVar[int] = 0

    PUBLISH_RUNNING: ClassVar[bool] = True
    SCAN_INTERVAL: ClassVar[float] = 0.02

    subscribe_feature_types: ClassVar[List[FeatureType]] = [
        FeatureType.DI,
        FeatureType.DO,
        FeatureType.RO,
    ]
    publish_feature_types: ClassVar[List[FeatureType]] = [
        FeatureType.DI,
        FeatureType.DO,
        FeatureType.RO,
        FeatureType.METER,
    ]
    publish_tcp_feature_types: ClassVar[List[FeatureType]] = [
        FeatureType.DI,
        FeatureType.DO,
        FeatureType.RO,
    ]
    publish_serial_feature_types: ClassVar[List[FeatureType]] = [
        FeatureType.DI,
        FeatureType.DO,
        FeatureType.RO,
        FeatureType.METER,
    ]

    def __init__(self, unipi: Unipi) -> None:
        self.config: Config = unipi.config
        self.unipi: Unipi = unipi

        self.covers: CoverMap = CoverMap(self.config, self.unipi.features)
        self.covers.init()

    async def run(self) -> None:
        """Connect/reconnect to MQTT broker."""
        mqtt_client_id: str = f"{slugify(self.config.device_info.name)}-{uuid.uuid4()}"
        UNIPI_LOGGER.info("%s Client ID: %s", LogPrefix.MQTT, mqtt_client_id)

        mqtt_client = MqttClient(
            self.config.mqtt.host,
            port=self.config.mqtt.port,
            username=self.config.mqtt.username,
            password=self.config.mqtt.password,
            client_id=mqtt_client_id,
            keepalive=self.config.mqtt.keepalive,
        )

        reconnect_interval: int = self.config.mqtt.reconnect_interval
        retry_limit: Optional[int] = self.config.mqtt.retry_limit
        retry_reconnect: int = 0
        discovery_initialized: bool = False

        while self.MQTT_RUNNING:
            tasks: Set[Task] = set()

            try:
                async with mqtt_client:
                    UNIPI_LOGGER.info(
                        "%s Connected to %s:%s", LogPrefix.MQTT, self.config.mqtt.host, self.config.mqtt.port
                    )

                    if self.config.homeassistant.enabled and not discovery_initialized:
                        UNIPI_LOGGER.info("%s Initialize Home Assistant discovery", LogPrefix.MQTT)
                        await self.discovery(client=mqtt_client)
                        discovery_initialized = True

                    tasks.add(asyncio.create_task(self.subscribe(client=mqtt_client)))
                    tasks.add(
                        asyncio.create_task(
                            self.publish(
                                client=mqtt_client,
                                feature_types=self.publish_tcp_feature_types,
                                scan_callback=self.unipi.modbus_helper.scan_tcp,
                                scan_interval=self.config.modbus_tcp.scan_interval,
                            )
                        )
                    )
                    tasks.add(
                        asyncio.create_task(
                            self.publish(
                                client=mqtt_client,
                                feature_types=self.publish_serial_feature_types,
                                scan_callback=self.unipi.modbus_helper.scan_serial,
                                scan_interval=self.config.modbus_serial.scan_interval,
                            )
                        )
                    )

                    CoversMqttHelper(
                        client=mqtt_client,
                        covers=self.covers,
                    ).init(tasks=tasks)

                    await asyncio.gather(*tasks)
            except MqttError as error:
                retry_reconnect += 1

                UNIPI_LOGGER.error(
                    "%s Error '%s'. Connecting attempt #%s. Reconnecting in %s seconds.",
                    LogPrefix.MQTT,
                    error,
                    retry_reconnect,
                    reconnect_interval,
                )

                if retry_limit and retry_reconnect >= retry_limit:
                    msg: str = "Shutdown, due to too many MQTT connection attempts."
                    raise UnexpectedError(msg) from error

                await asyncio.sleep(reconnect_interval)
            else:
                retry_reconnect = 0

    async def subscribe(self, client: MqttClient) -> None:
        """Subscribe feature topics to MQTT."""
        
        topics = set([f"{slugify(unit.config.device_info.name)}/#" for unit in self.unipi.unipi_boards])
        topics_with_qos = [(topic, 0) for topic in topics]
        async with client.messages() as messages:
            await client.subscribe(topics_with_qos)

            async for message in messages:
                for unit in self.unipi.unipi_boards:
                    for feature in unit.features.by_feature_types(self.subscribe_feature_types):
                        topic: str = f"{feature.topic}/set"

                        if message.topic.matches(topic) and (payload := message.payload) and isinstance(payload, bytes):
                            value: str = payload.decode()
                            print(f"SUB: {message.topic} : {value}")
                            if isinstance(feature, (DigitalOutput, Relay)):
                                if value == "ON":
                                    await feature.set_state(True)
                                elif value == "OFF":
                                    await feature.set_state(False)

                                if (
                                    value in {"ON", "OFF"}
                                    and LOG_LEVEL[self.unipi.config.logging.mqtt.features_level] <= LOG_LEVEL["info"]
                                ):
                                    UNIPI_LOGGER.log(
                                        level=LOG_LEVEL["info"],
                                        msg=LOG_MQTT_SUBSCRIBE % (topic, value),
                                    )

        await asyncio.sleep(self.SCAN_INTERVAL)

    async def publish(
        self,
        client: MqttClient,
        feature_types: List[FeatureType],
        scan_callback: Callable[..., Awaitable[None]],
        scan_interval: float,
    ) -> None:
        """Publish feature changes to MQTT."""
        while self.PUBLISH_RUNNING:
            await scan_callback()
            for unit in self.unipi.unipi_boards:
                for feature in unit.features.by_feature_types(feature_types):
                    if feature.changed:
                        topic: str = f"{feature.topic}/get"
                        print(f"PUB: {topic} : {feature.payload}")
                        await client.publish(topic=topic, payload=feature.payload, qos=1, retain=True)

                        if (
                            isinstance(feature, Eastron)
                            and LOG_LEVEL[self.unipi.config.logging.mqtt.meters_level] <= LOG_LEVEL["info"]
                        ) or (
                            isinstance(feature, (DigitalInput, DigitalOutput, Led, Relay))
                            and LOG_LEVEL[self.unipi.config.logging.mqtt.features_level] <= LOG_LEVEL["info"]
                        ):
                            UNIPI_LOGGER.log(
                                level=LOG_LEVEL["info"],
                                msg=LOG_MQTT_PUBLISH % (topic, feature.payload),
                            )

            await asyncio.sleep(scan_interval)

    async def discovery(self, client: MqttClient) -> None:
        """Publish MQTT Home Assistant discovery topics."""
        for unit in self.unipi.unipi_boards:
            for feature in unit.features.by_feature_types(self.publish_feature_types):
                if isinstance(feature, DigitalInput):
                    await HassBinarySensorsDiscovery(unipi_board=unit, client=client).publish(feature)
                elif isinstance(feature, Eastron):
                    await HassSensorsDiscovery(unipi_board=unit, client=client).publish(feature)
                elif isinstance(feature, (DigitalOutput, Relay)):
                    await HassSwitchesDiscovery(unipi_board=unit, client=client).publish(feature)

            await HassCoversDiscovery(covers=self.covers, unipi_board=unit, client=client).publish()
