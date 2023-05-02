import logging
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncGenerator
from typing import NamedTuple
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import PropertyMock

import pytest
import pytest_asyncio
from _pytest.fixtures import SubRequest  # pylint: disable=import-private-name
from pymodbus.pdu import ModbusResponse
from pytest_mock import MockerFixture

from unipi_control.config import Config
from unipi_control.integrations.covers import CoverMap
from unipi_control.modbus import ModbusClient
from unipi_control.neuron import Neuron
from unittests.conftest_data import EXTENSION_EASTRON_SDM120M_MODBUS_REGISTER
from unittests.conftest_data import NEURON_L203_MODBUS_REGISTER


@pytest.fixture(autouse=True, scope="session")
def logger() -> None:
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger().handlers.clear()
    logging.info("Initialize logging")


class ConfigLoader:
    def __init__(self, temp: Path) -> None:
        self.temp: Path = temp
        self.config_file_path: Path = self.temp / "control.yaml"

        hardware_data_path: Path = self.temp / "hardware/neuron"
        hardware_data_path.mkdir(parents=True)
        self.hardware_data_file_path = hardware_data_path / "MOCKED_MODEL.yaml"

        extension_hardware_data_path: Path = self.temp / "hardware/extensions"
        extension_hardware_data_path.mkdir(parents=True)
        self.extension_hardware_data_file_path = extension_hardware_data_path / "MOCKED_EASTRON.yaml"

        self.temp_path: Path = self.temp / "unipi"
        self.temp_path.mkdir(parents=True)

    def write_config(self, content: str) -> None:
        with self.config_file_path.open("w", encoding="utf-8") as _file:
            _file.write(content)

    def write_hardware_data(self, content: str) -> None:
        with self.hardware_data_file_path.open("w", encoding="utf-8") as _file:
            _file.write(content)

    def write_extension_hardware_data(self, content: str) -> None:
        with self.extension_hardware_data_file_path.open("w", encoding="utf-8") as _file:
            _file.write(content)

    def get_config(self) -> Config:
        return Config(config_base_path=self.temp, temp_path=self.temp_path)


@pytest.fixture()
def _config_loader(request: SubRequest, tmp_path: Path) -> ConfigLoader:
    config_loader: ConfigLoader = ConfigLoader(temp=tmp_path)
    config_loader.write_config(request.param[0])
    config_loader.write_hardware_data(request.param[1])
    config_loader.write_extension_hardware_data(request.param[2])

    logging.info("Create configuration: %s", tmp_path)

    return config_loader


@dataclass
class MockHardwareInfo:
    name: str = "MOCKED_NAME"
    model: str = "MOCKED_MODEL"
    version: str = "MOCKED_VERSION"
    serial: str = "MOCKED_SERIAL"


class MockModbusClient(NamedTuple):
    tcp: AsyncMock
    serial: AsyncMock


@pytest.fixture()
def _modbus_client(mocker: MockerFixture) -> MockModbusClient:
    mock_bord_response: MagicMock = MagicMock(spec=ModbusResponse, registers=[0])
    mock_bord_response.isError.return_value = False

    for mock_response in NEURON_L203_MODBUS_REGISTER:
        mock_response.isError.return_value = False

    mock_modbus_tcp_client: AsyncMock = AsyncMock()
    mock_modbus_tcp_client.read_input_registers.side_effect = [
        # Board 1
        mock_bord_response,
        # Board 2
        mock_bord_response,
        # Board 3
        mock_bord_response,
    ] + NEURON_L203_MODBUS_REGISTER

    for mock_response in EXTENSION_EASTRON_SDM120M_MODBUS_REGISTER:
        mock_response.isError.return_value = False

    mock_modbus_serial_client: AsyncMock = AsyncMock()
    mock_modbus_serial_client.read_input_registers.side_effect = EXTENSION_EASTRON_SDM120M_MODBUS_REGISTER

    mock_response_sw_version: MagicMock = MagicMock(spec=ModbusResponse, registers=[32, 516])
    mock_response_sw_version.isError.return_value = False

    mock_modbus_serial_client.read_holding_registers.side_effect = [
        # Eastron SDM120M Software Version
        mock_response_sw_version
    ]

    mock_hardware_info: PropertyMock = mocker.patch("unipi_control.config.HardwareInfo", new_callable=PropertyMock())
    mock_hardware_info.return_value = MockHardwareInfo()

    return MockModbusClient(tcp=mock_modbus_tcp_client, serial=mock_modbus_serial_client)


@pytest_asyncio.fixture()
async def _neuron(_config_loader: ConfigLoader, _modbus_client: ModbusClient) -> AsyncGenerator:
    config: Config = _config_loader.get_config()

    _neuron: Neuron = Neuron(config=config, modbus_client=_modbus_client)
    await _neuron.init()

    yield _neuron


@pytest_asyncio.fixture()
async def _covers(_config_loader: ConfigLoader, _neuron: Neuron) -> AsyncGenerator:
    config: Config = _config_loader.get_config()
    yield CoverMap(config=config, features=_neuron.features)


class MockMQTTMessage(NamedTuple):
    payload: bytes


class MockMQTTMessages:
    def __init__(self, message) -> None:
        self.message = message

    def __aiter__(self):
        return self

    async def __anext__(self) -> MockMQTTMessage:
        if self.message:
            return MockMQTTMessage(self.message.pop())

        raise StopAsyncIteration