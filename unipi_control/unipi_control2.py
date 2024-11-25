"""Unipi Control entry point for read configuration, initialize modbus and connect to mqtt."""

import argparse
import asyncio
import sys
from pathlib import Path

from pymodbus.client import AsyncModbusTcpClient, AsyncModbusSerialClient
from typing import List, Optional
from unipi_control.config import Config, DEFAULT_CONFIG_DIR, LogPrefix
from unipi_control.config import UNIPI_LOGGER
from unipi_control.helpers.argparse import init_argparse
from unipi_control.helpers.exceptions import ConfigError, UnexpectedError
from unipi_control.modbus.helpers import ModbusClient
from unipi_control.mqtt.helpers import MqttHelper
from unipi_control.hardware.unipi import Unipi
from unipi_control.version import __version__

class UnipiControl:
    """Control Unipi I/O directly with MQTT commands.

    Unipi Control use Modbus for fast access to the I/O and provide MQTT
    topics for reading and writing the circuits. Optionally you can enable
    the Home Assistant MQTT discovery for binary sensors, sensors, switches,
    lights and covers.
    """

    def __init__(self, config: Config, modbus_client: ModbusClient) -> None:
        self.config: Config = config
        self.modbus_client: ModbusClient = modbus_client
        self.unipi: Unipi = Unipi(config=config, modbus_client=modbus_client)
        
    @classmethod
    def parse_args(cls, args: List[str]) -> argparse.Namespace:
        """Initialize argument parser options.

        Parameters
        ----------
        args: list
            Arguments as list.

        Returns
        -------
        Argparse namespace
        """
        parser: argparse.ArgumentParser = init_argparse(description="Control Unipi I/O with MQTT commands")
        parser.add_argument(
            "-c",
            "--config",
            action="store",
            default=DEFAULT_CONFIG_DIR,
            help=f"path to the configuration (default: {DEFAULT_CONFIG_DIR})",
        )

        parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

        return parser.parse_args(args)

    async def run(self) -> None:
        """Connect to Modbus/MQTT and initialize hardware features."""
        await self.unipi.init()
        await MqttHelper(unipi=self.unipi).run()


async def main(argv: Optional[List[str]] = None) -> None:
#    import debugpy
#    debugpy.listen(("0.0.0.0", 5678))
#    print("Waiting for debugger attach...")
#    debugpy.wait_for_client()
#    print("Debugger attached")
    
    """Entrypoint for Unipi Control."""
    if argv is None:
        argv = sys.argv[1:]

    unipi_control: Optional[UnipiControl] = None
    args: argparse.Namespace = UnipiControl.parse_args(argv)

    try:
        config: Config = Config(config_base_dir=Path(args.config))
        config.logging.init(log=args.log, verbose=args.verbose)

        async with AsyncModbusTcpClient(
            host=config.modbus_tcp.host,
            port=config.modbus_tcp.port,
        ) as tcp_client, AsyncModbusSerialClient(
            port=config.modbus_serial.port,
            baudrate=config.modbus_serial.baud_rate,
            parity=config.modbus_serial.parity,
            stopbits=1,
            timeout=1,
            bytesize=8
        ) as serial_client:
            await tcp_client.connect()
            await serial_client.connect()
            unipi_control = UnipiControl(
                config=config,
                modbus_client=ModbusClient(tcp=tcp_client, serial=serial_client),
            )

            await unipi_control.run()
    except ConfigError as error:
        UNIPI_LOGGER.critical("%s %s", LogPrefix.CONFIG, error)
        sys.exit(1)
    except UnexpectedError as error:
        UNIPI_LOGGER.critical(error)
        sys.exit(1)
    except KeyboardInterrupt:
        UNIPI_LOGGER.info("Received exit, exiting")
    except asyncio.CancelledError:
        ...
    finally:
        if unipi_control:
            UNIPI_LOGGER.info("Successfully shutdown the Unipi Control service.")

if __name__ == "__main__":
    asyncio.run(main())
