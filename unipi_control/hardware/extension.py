from unipi_control.config import Config
from unipi_control.hardware.map import HardwareDefinition
from unipi_control.modbus.helpers import ModbusClient
from unipi_control.modbus.helpers import ModbusHelper
from unipi_control.features.map import FeatureMap
from unipi_control.hardware.unipi_board import UnipiBoard
from unipi_control.hardware.unipi_board import UnipiBoardConfig


class Extension(UnipiBoard):
    def __init__(
        self,
        config: Config,
        modbus_client: ModbusClient,
        modbus_helper: ModbusHelper,
        definition: HardwareDefinition,
        features: FeatureMap,
        board_config: UnipiBoardConfig,
    ) -> None:
        self.config: Config = config
        self.modbus_client: ModbusClient = modbus_client
        self.modbus_helper: ModbusHelper = modbus_helper
        self.definition: HardwareDefinition = definition
        self.features: FeatureMap = features
        self.board_config: UnipiBoardConfig = board_config
