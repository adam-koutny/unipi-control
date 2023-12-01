"""Initialize MQTT subscribe and publish for Home Assistant binary sensors."""

import json
from typing import Any
from typing import Dict
from typing import TYPE_CHECKING
from typing import Tuple

from unipi_control.config import UNIPI_LOGGER
from unipi_control.features.unipi import DigitalInput
from unipi_control.features.unipi import UnipiFeature
from unipi_control.features.constants import FeatureState
from unipi_control.helpers.log import LOG_MQTT_PUBLISH
from unipi_control.helpers.text import slugify
from unipi_control.mqtt.discovery.mixin import HassDiscoveryMixin

if TYPE_CHECKING:
    from unipi_control.hardware.map import HardwareDefinition


class HassBinarySensorsDiscovery(HassDiscoveryMixin):
    """Provide the binary sensors (e.g. digital input) as Home Assistant MQTT discovery."""

    def _get_device_name(self, feature: UnipiFeature) -> str:
        device_name: str = self.config.device_info.name
        definition: HardwareDefinition = feature.hardware.definition

        if definition.device_name:
            device_name = definition.device_name

        return device_name

    def get_discovery(self, feature: DigitalInput) -> Tuple[str, Dict[str, Any]]:
        """Get MQTT topic and message for publish with mqtt.

        Parameters
        ----------
        feature:
            All input features.

        Returns
        -------
        tuple:
            Return mqtt topic and message as tuple.
        """
        topic: str = (
            f"{self.config.homeassistant.discovery_prefix}/binary_sensor"
            f"/{slugify(self.config.device_info.name)}/{feature.object_id}/config"
        )
        device_name: str = self._get_device_name(feature)

        message: Dict[str, Any] = {
            "name": feature.friendly_name,
            "unique_id": feature.unique_id,
            "state_topic": f"{feature.topic}/get",
            "qos": 2,
            "device": {
                "name": device_name,
                "identifiers": slugify(device_name),
                "model": self._get_device_model(feature),
                "sw_version": feature.sw_version,
                "manufacturer": self._get_device_manufacturer(feature),
            },
        }

        if feature.object_id:
            message["object_id"] = feature.object_id

        if feature.icon:
            message["icon"] = feature.icon

        if feature.device_class:
            message["device_class"] = feature.device_class

        if self._get_invert_state(feature):
            message["payload_on"] = FeatureState.OFF
            message["payload_off"] = FeatureState.ON

        if self.config.device_info.suggested_area:
            message["device"]["suggested_area"] = self.config.device_info.suggested_area

        return topic, message

    async def publish(self, feature: DigitalInput) -> None:
        """Publish MQTT Home Assistant discovery topics for binary sensors."""
        topic, message = self.get_discovery(feature)
        json_data: str = json.dumps(message)
        await self.client.publish(topic=topic, payload=json_data, qos=2, retain=True)
        UNIPI_LOGGER.debug(LOG_MQTT_PUBLISH, topic, json_data)
