"""Unit test for configurations."""
import logging
import re
from pathlib import Path
from typing import List
from typing import NamedTuple
from typing import Optional

import pytest
from _pytest.capture import CaptureFixture
from _pytest.logging import LogCaptureFixture

from tests.conftest import ConfigLoader
from tests.conftest_data import CONFIG_CONTENT
from tests.conftest_data import CONFIG_CONTENT_WITHOUT_PERSISTENT_TMP_DIR
from tests.conftest_data import CONFIG_CONTENT_WITH_PERSISTENT_TMP_DIR
from tests.conftest_data import EXTENSION_HARDWARE_DATA_CONTENT
from tests.conftest_data import HARDWARE_DATA_CONTENT
from tests.unit.test_config_data import CONFIG_DUPLICATE_COVERS_CIRCUITS
from tests.unit.test_config_data import CONFIG_DUPLICATE_COVER_ID
from tests.unit.test_config_data import CONFIG_DUPLICATE_MODBUS_UNIT
from tests.unit.test_config_data import CONFIG_DUPLICATE_OBJECT_ID
from tests.unit.test_config_data import CONFIG_INVALID
from tests.unit.test_config_data import CONFIG_INVALID_COVER_ID
from tests.unit.test_config_data import CONFIG_INVALID_COVER_TYPE
from tests.unit.test_config_data import CONFIG_INVALID_DEVICE_CLASS
from tests.unit.test_config_data import CONFIG_INVALID_DEVICE_NAME
from tests.unit.test_config_data import CONFIG_INVALID_FEATURE_ID
from tests.unit.test_config_data import CONFIG_INVALID_FEATURE_TYPE
from tests.unit.test_config_data import CONFIG_INVALID_HOMEASSISTANT_DISCOVERY_PREFIX
from tests.unit.test_config_data import CONFIG_INVALID_LOG_LEVEL
from tests.unit.test_config_data import CONFIG_INVALID_MODBUS_BAUD_RATE
from tests.unit.test_config_data import CONFIG_INVALID_MODBUS_PARITY
from tests.unit.test_config_data import CONFIG_INVALID_MQTT_PORT_TYPE
from tests.unit.test_config_data import CONFIG_INVALID_PERSISTENT_TMP_DIR
from tests.unit.test_config_data import CONFIG_LOGGING_LEVEL_ERROR
from tests.unit.test_config_data import CONFIG_LOGGING_LEVEL_INFO
from tests.unit.test_config_data import CONFIG_MISSING_COVER_KEY
from tests.unit.test_config_data import CONFIG_MISSING_DEVICE_NAME
from unipi_control.config import Config
from unipi_control.config import UNIPI_LOGGER
from unipi_control.helpers.exceptions import ConfigError
from unipi_control.helpers.log import SIMPLE_LOG_FORMAT
from unipi_control.modbus.helpers import ModbusClient
from unipi_control.hardware.unipi import Unipi


class LoggingLevelParams(NamedTuple):
    log: Optional[str]
    verbose: int


class LoggingOutputParams(NamedTuple):
    level: int
    log: str
    fmt: Optional[str]
    message: str


class TestHappyPathConfig:
    @pytest.mark.parametrize(
        ("config_loader", "params", "expected"),
        [
            (
                [CONFIG_LOGGING_LEVEL_INFO, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT],
                LoggingLevelParams(log="stdout", verbose=0),
                logging.INFO,
            ),
            (
                [CONFIG_LOGGING_LEVEL_INFO, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT],
                LoggingLevelParams(log="systemd", verbose=0),
                logging.INFO,
            ),
            (
                [CONFIG_LOGGING_LEVEL_INFO, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT],
                LoggingLevelParams(log=None, verbose=0),
                logging.INFO,
            ),
            (
                [CONFIG_LOGGING_LEVEL_INFO, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT],
                LoggingLevelParams(log="systemd", verbose=1),
                logging.INFO,
            ),
            (
                [CONFIG_LOGGING_LEVEL_INFO, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT],
                LoggingLevelParams(log="systemd", verbose=2),
                logging.INFO,
            ),
            (
                [CONFIG_LOGGING_LEVEL_INFO, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT],
                LoggingLevelParams(log="systemd", verbose=3),
                logging.DEBUG,
            ),
            (
                [CONFIG_LOGGING_LEVEL_ERROR, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT],
                LoggingLevelParams(log="stdout", verbose=0),
                logging.ERROR,
            ),
            (
                [CONFIG_LOGGING_LEVEL_ERROR, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT],
                LoggingLevelParams(log="systemd", verbose=0),
                logging.ERROR,
            ),
            (
                [CONFIG_LOGGING_LEVEL_ERROR, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT],
                LoggingLevelParams(log=None, verbose=0),
                logging.ERROR,
            ),
            (
                [CONFIG_LOGGING_LEVEL_ERROR, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT],
                LoggingLevelParams(log="systemd", verbose=1),
                logging.WARNING,
            ),
            (
                [CONFIG_LOGGING_LEVEL_ERROR, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT],
                LoggingLevelParams(log="systemd", verbose=2),
                logging.INFO,
            ),
            (
                [CONFIG_LOGGING_LEVEL_ERROR, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT],
                LoggingLevelParams(log="systemd", verbose=3),
                logging.DEBUG,
            ),
        ],
        indirect=["config_loader"],
    )
    def test_logging_level(self, config_loader: ConfigLoader, params: LoggingLevelParams, expected: int) -> None:
        """Test verbose arguments change log level."""
        config: Config = config_loader.get_config()
        config.logging.init(log=params.log, verbose=params.verbose)

        assert UNIPI_LOGGER.level == expected

    @pytest.mark.parametrize(
        ("config_loader", "params", "expected"),
        [
            (
                CONFIG_LOGGING_LEVEL_INFO,
                LoggingOutputParams(level=logging.CRITICAL, log="stdout", fmt=None, message="MOCKED MESSAGE"),
                r"^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2},\d{3} \| CRITICAL \| MOCKED MESSAGE\n$",
            ),
            (
                CONFIG_LOGGING_LEVEL_INFO,
                LoggingOutputParams(
                    level=logging.CRITICAL, log="stdout", fmt=SIMPLE_LOG_FORMAT, message="MOCKED MESSAGE"
                ),
                r"^MOCKED MESSAGE\n$",
            ),
            (
                CONFIG_LOGGING_LEVEL_INFO,
                LoggingOutputParams(level=logging.CRITICAL, log="systemd", fmt=None, message="MOCKED MESSAGE"),
                r"<2>MOCKED MESSAGE\n",
            ),
            (
                CONFIG_LOGGING_LEVEL_INFO,
                LoggingOutputParams(level=logging.ERROR, log="systemd", fmt=None, message="MOCKED MESSAGE"),
                r"<3>MOCKED MESSAGE\n",
            ),
            (
                CONFIG_LOGGING_LEVEL_INFO,
                LoggingOutputParams(level=logging.WARNING, log="systemd", fmt=None, message="MOCKED MESSAGE"),
                r"<4>MOCKED MESSAGE\n",
            ),
            (
                CONFIG_LOGGING_LEVEL_INFO,
                LoggingOutputParams(level=logging.INFO, log="systemd", fmt=None, message="MOCKED MESSAGE"),
                r"<6>MOCKED MESSAGE\n",
            ),
            (
                CONFIG_LOGGING_LEVEL_INFO,
                LoggingOutputParams(level=logging.DEBUG, log="systemd", fmt=None, message="MOCKED MESSAGE"),
                r"<7>MOCKED MESSAGE\n",
            ),
        ],
        indirect=["config_loader"],
    )
    def test_logging_output(
        self, config_loader: ConfigLoader, params: LoggingOutputParams, expected: str, capsys: CaptureFixture
    ) -> None:
        """Test log handler output."""
        config: Config = config_loader.get_config()
        config.logging.init(log=params.log, verbose=3, fmt=params.fmt)

        UNIPI_LOGGER.log(level=params.level, msg=params.message)

        assert re.compile(expected).search(capsys.readouterr().err)

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        "config_loader",
        [
            (CONFIG_CONTENT, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
        ],
        indirect=["config_loader"],
    )
    async def test_hardware_definition_found(
        self, config_loader: ConfigLoader, modbus_client: ModbusClient, caplog: LogCaptureFixture
    ) -> None:
        """Test hardware definition found."""
        config: Config = config_loader.get_config()
        config.logging.init()

        unipi: Unipi = Unipi(config=config, modbus_client=modbus_client)
        await unipi.init()

        logs: List[str] = [record.getMessage() for record in caplog.records]
        assert "[CONFIG] 2 hardware definition(s) found." in logs

    @pytest.mark.asyncio()
    @pytest.mark.parametrize(
        ("config_loader", "expected"),
        [
            (
                (CONFIG_CONTENT_WITH_PERSISTENT_TMP_DIR, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "/var/tmp/unipi",
            ),
            (
                (CONFIG_CONTENT_WITHOUT_PERSISTENT_TMP_DIR, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "/tmp/unipi",
            ),
        ],
        indirect=["config_loader"],
    )
    def test_unipi_tmp_dir(self, config_loader: ConfigLoader, expected: str) -> None:
        """Test persistent temporary directory."""
        config: Config = config_loader.get_config(set_unipi_tmp_dir=False)
        config.logging.init()

        assert config.unipi_tmp_dir == Path(expected)


class TestUnhappyPathConfig:
    @pytest.mark.parametrize(
        ("config_loader", "expected"),
        [
            (
                (CONFIG_INVALID_DEVICE_NAME, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "[DEVICEINFO] Invalid value 'INVALID DEVICE NAME$' in 'name'. "
                "The following characters are prohibited: a-z 0-9 -_ space",
            ),
            (
                (
                    CONFIG_INVALID_HOMEASSISTANT_DISCOVERY_PREFIX,
                    HARDWARE_DATA_CONTENT,
                    EXTENSION_HARDWARE_DATA_CONTENT,
                ),
                "[HOMEASSISTANT] Invalid value 'invalid discovery name' in 'discovery_prefix'. "
                "The following characters are prohibited: a-z 0-9 -_",
            ),
            (
                (CONFIG_INVALID_FEATURE_TYPE, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "Expected features to be <class 'dict'>, got 'INVALID'",
            ),
            (
                (CONFIG_INVALID_COVER_TYPE, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "Expected covers to be <class 'list'>, got 'INVALID'",
            ),
            (
                (CONFIG_INVALID_MQTT_PORT_TYPE, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "Expected port to be <class 'int'>, got 'INVALID'",
            ),
            (
                (CONFIG_INVALID_COVER_ID, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "[COVER] Invalid value 'invalid id' in 'object_id'. "
                "The following characters are prohibited: a-z 0-9 -_",
            ),
            (
                (CONFIG_INVALID_DEVICE_CLASS, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "[COVER] Invalid value 'INVALID' in 'device_class'. "
                "The following values are allowed: awning curtain door garage gate shade blind shutter window.",
            ),
            (
                (CONFIG_MISSING_COVER_KEY, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "[COVER] Required key 'object_id' is missing! "
                "CoverConfig(object_id='', friendly_name='MOCKED_FRIENDLY_NAME - BLIND', suggested_area='', "
                "device_class='blind', cover_run_time=35.5, tilt_change_time=1.5, cover_up='ro_3_01', "
                "cover_down='ro_3_02')",
            ),
            (
                (CONFIG_DUPLICATE_COVERS_CIRCUITS, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "[COVER] Duplicate circuits found in 'covers'. "
                "Driving both signals up and down at the same time can damage the motor!",
            ),
            (
                (CONFIG_INVALID, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                'Can\'t read YAML file!\n  in "<unicode string>", line 2, column 21:\n'
                "      name: MOCKED UNIPI:\n                        ^",
            ),
            (
                (CONFIG_INVALID_LOG_LEVEL, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "[LOGGING] Invalid log level 'invalid'. "
                "The following log levels are allowed: error warning info debug.",
            ),
            (
                (CONFIG_DUPLICATE_COVER_ID, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "[COVER] Duplicate ID 'mocked_duplicate_id' found in 'covers'!",
            ),
            (
                (CONFIG_DUPLICATE_OBJECT_ID, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "[FEATURE] Duplicate ID 'mocked_duplicate_id' found in 'features'!",
            ),
            (
                (CONFIG_INVALID_FEATURE_ID, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "[FEATURE] Invalid value 'invalid id' in 'object_id'. "
                "The following characters are prohibited: a-z 0-9 -_",
            ),
            (
                (CONFIG_INVALID_MODBUS_BAUD_RATE, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "[MODBUS] Invalid baud rate '2401'. "
                "The following baud rates are allowed: 2400 4800 9600 19200 38400 57600 115200.",
            ),
            (
                (CONFIG_INVALID_MODBUS_PARITY, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "[MODBUS] Invalid value 'S' in 'parity'. The following parity options are allowed: E O N.",
            ),
            (
                (CONFIG_DUPLICATE_MODBUS_UNIT, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "[MODBUS] Duplicate modbus unit '1' found in 'units'!",
            ),
            (
                (CONFIG_MISSING_DEVICE_NAME, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "[MODBUS] Device name for unit '1' is missing!",
            ),
            (
                (CONFIG_INVALID_PERSISTENT_TMP_DIR, HARDWARE_DATA_CONTENT, EXTENSION_HARDWARE_DATA_CONTENT),
                "Expected persistent_tmp_dir to be <class 'bool'>, got 'invalid'",
            ),
        ],
        indirect=["config_loader"],
    )
    def test_validation(self, config_loader: ConfigLoader, expected: str) -> None:
        """Test yaml config raises ConfigError when validation failed."""
        with pytest.raises(ConfigError) as error:
            config_loader.get_config()

        assert str(error.value) == expected
