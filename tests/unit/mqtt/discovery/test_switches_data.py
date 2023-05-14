from typing import Any
from typing import Dict
from typing import List

discovery_message_expected: List[Dict[str, Any]] = [
    {
        "message": {
            "name": "MOCKED UNIPI: Digital Output 1.01",
            "unique_id": "mocked_unipi_do_1_01",
            "command_topic": "mocked_unipi/relay/do_1_01/set",
            "state_topic": "mocked_unipi/relay/do_1_01/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_do_1_01/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Digital Output 1.02",
            "unique_id": "mocked_unipi_do_1_02",
            "command_topic": "mocked_unipi/relay/do_1_02/set",
            "state_topic": "mocked_unipi/relay/do_1_02/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_do_1_02/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Digital Output 1.03",
            "unique_id": "mocked_unipi_do_1_03",
            "command_topic": "mocked_unipi/relay/do_1_03/set",
            "state_topic": "mocked_unipi/relay/do_1_03/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_do_1_03/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Digital Output 1.04",
            "unique_id": "mocked_unipi_do_1_04",
            "command_topic": "mocked_unipi/relay/do_1_04/set",
            "state_topic": "mocked_unipi/relay/do_1_04/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_do_1_04/config",
    },
    {
        "message": {
            "name": "MOCKED_FRIENDLY_NAME - RO_2_01",
            "unique_id": "mocked_unipi_mocked_id_ro_2_01",
            "command_topic": "mocked_unipi/relay/ro_2_01/set",
            "state_topic": "mocked_unipi/relay/ro_2_01/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI - MOCKED AREA 2",
                "identifiers": "MOCKED UNIPI - MOCKED AREA 2",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
                "suggested_area": "MOCKED AREA 2",
                "via_device": "MOCKED UNIPI",
            },
            "object_id": "mocked_id_ro_2_01",
            "payload_on": "OFF",
            "payload_off": "ON",
        },
        "topic": "homeassistant/switch/mocked_unipi_mocked_id_ro_2_01/config",
    },
    {
        "message": {
            "name": "MOCKED_FRIENDLY_NAME - RO_2_02",
            "unique_id": "mocked_unipi_mocked_id_ro_2_02",
            "command_topic": "mocked_unipi/relay/ro_2_02/set",
            "state_topic": "mocked_unipi/relay/ro_2_02/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI - MOCKED AREA 2",
                "identifiers": "MOCKED UNIPI - MOCKED AREA 2",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
                "suggested_area": "MOCKED AREA 2",
                "via_device": "MOCKED UNIPI",
            },
            "object_id": "mocked_id_ro_2_02",
            "device_class": "switch",
            "icon": "mdi:power-standby",
        },
        "topic": "homeassistant/switch/mocked_unipi_mocked_id_ro_2_02/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 2.03",
            "unique_id": "mocked_unipi_ro_2_03",
            "command_topic": "mocked_unipi/relay/ro_2_03/set",
            "state_topic": "mocked_unipi/relay/ro_2_03/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_2_03/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 2.04",
            "unique_id": "mocked_unipi_ro_2_04",
            "command_topic": "mocked_unipi/relay/ro_2_04/set",
            "state_topic": "mocked_unipi/relay/ro_2_04/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_2_04/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 2.05",
            "unique_id": "mocked_unipi_ro_2_05",
            "command_topic": "mocked_unipi/relay/ro_2_05/set",
            "state_topic": "mocked_unipi/relay/ro_2_05/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_2_05/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 2.06",
            "unique_id": "mocked_unipi_ro_2_06",
            "command_topic": "mocked_unipi/relay/ro_2_06/set",
            "state_topic": "mocked_unipi/relay/ro_2_06/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_2_06/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 2.07",
            "unique_id": "mocked_unipi_ro_2_07",
            "command_topic": "mocked_unipi/relay/ro_2_07/set",
            "state_topic": "mocked_unipi/relay/ro_2_07/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_2_07/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 2.08",
            "unique_id": "mocked_unipi_ro_2_08",
            "command_topic": "mocked_unipi/relay/ro_2_08/set",
            "state_topic": "mocked_unipi/relay/ro_2_08/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_2_08/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 2.09",
            "unique_id": "mocked_unipi_ro_2_09",
            "command_topic": "mocked_unipi/relay/ro_2_09/set",
            "state_topic": "mocked_unipi/relay/ro_2_09/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_2_09/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 2.10",
            "unique_id": "mocked_unipi_ro_2_10",
            "command_topic": "mocked_unipi/relay/ro_2_10/set",
            "state_topic": "mocked_unipi/relay/ro_2_10/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_2_10/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 2.11",
            "unique_id": "mocked_unipi_ro_2_11",
            "command_topic": "mocked_unipi/relay/ro_2_11/set",
            "state_topic": "mocked_unipi/relay/ro_2_11/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_2_11/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 2.12",
            "unique_id": "mocked_unipi_ro_2_12",
            "command_topic": "mocked_unipi/relay/ro_2_12/set",
            "state_topic": "mocked_unipi/relay/ro_2_12/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_2_12/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 2.13",
            "unique_id": "mocked_unipi_ro_2_13",
            "command_topic": "mocked_unipi/relay/ro_2_13/set",
            "state_topic": "mocked_unipi/relay/ro_2_13/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_2_13/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 2.14",
            "unique_id": "mocked_unipi_ro_2_14",
            "command_topic": "mocked_unipi/relay/ro_2_14/set",
            "state_topic": "mocked_unipi/relay/ro_2_14/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_2_14/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.01",
            "unique_id": "mocked_unipi_ro_3_01",
            "command_topic": "mocked_unipi/relay/ro_3_01/set",
            "state_topic": "mocked_unipi/relay/ro_3_01/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_01/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.02",
            "unique_id": "mocked_unipi_ro_3_02",
            "command_topic": "mocked_unipi/relay/ro_3_02/set",
            "state_topic": "mocked_unipi/relay/ro_3_02/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_02/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.03",
            "unique_id": "mocked_unipi_ro_3_03",
            "command_topic": "mocked_unipi/relay/ro_3_03/set",
            "state_topic": "mocked_unipi/relay/ro_3_03/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_03/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.04",
            "unique_id": "mocked_unipi_ro_3_04",
            "command_topic": "mocked_unipi/relay/ro_3_04/set",
            "state_topic": "mocked_unipi/relay/ro_3_04/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_04/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.05",
            "unique_id": "mocked_unipi_ro_3_05",
            "command_topic": "mocked_unipi/relay/ro_3_05/set",
            "state_topic": "mocked_unipi/relay/ro_3_05/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_05/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.06",
            "unique_id": "mocked_unipi_ro_3_06",
            "command_topic": "mocked_unipi/relay/ro_3_06/set",
            "state_topic": "mocked_unipi/relay/ro_3_06/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_06/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.07",
            "unique_id": "mocked_unipi_ro_3_07",
            "command_topic": "mocked_unipi/relay/ro_3_07/set",
            "state_topic": "mocked_unipi/relay/ro_3_07/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_07/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.08",
            "unique_id": "mocked_unipi_ro_3_08",
            "command_topic": "mocked_unipi/relay/ro_3_08/set",
            "state_topic": "mocked_unipi/relay/ro_3_08/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_08/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.09",
            "unique_id": "mocked_unipi_ro_3_09",
            "command_topic": "mocked_unipi/relay/ro_3_09/set",
            "state_topic": "mocked_unipi/relay/ro_3_09/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_09/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.10",
            "unique_id": "mocked_unipi_ro_3_10",
            "command_topic": "mocked_unipi/relay/ro_3_10/set",
            "state_topic": "mocked_unipi/relay/ro_3_10/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_10/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.11",
            "unique_id": "mocked_unipi_ro_3_11",
            "command_topic": "mocked_unipi/relay/ro_3_11/set",
            "state_topic": "mocked_unipi/relay/ro_3_11/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_11/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.12",
            "unique_id": "mocked_unipi_ro_3_12",
            "command_topic": "mocked_unipi/relay/ro_3_12/set",
            "state_topic": "mocked_unipi/relay/ro_3_12/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_12/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.13",
            "unique_id": "mocked_unipi_ro_3_13",
            "command_topic": "mocked_unipi/relay/ro_3_13/set",
            "state_topic": "mocked_unipi/relay/ro_3_13/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_13/config",
    },
    {
        "message": {
            "name": "MOCKED UNIPI: Relay 3.14",
            "unique_id": "mocked_unipi_ro_3_14",
            "command_topic": "mocked_unipi/relay/ro_3_14/set",
            "state_topic": "mocked_unipi/relay/ro_3_14/get",
            "qos": 2,
            "device": {
                "name": "MOCKED UNIPI",
                "identifiers": "MOCKED UNIPI",
                "model": "MOCKED_NAME MOCKED_MODEL",
                "sw_version": "0.0",
                "manufacturer": "Unipi technology",
            },
        },
        "topic": "homeassistant/switch/mocked_unipi_ro_3_14/config",
    },
]
