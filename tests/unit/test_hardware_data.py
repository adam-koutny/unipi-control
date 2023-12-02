"""Data for hardware unit tests."""

from typing import Final

HARDWARE_DATA_INVALID_KEY: Final[
    str
] = """modbus_register_block:
    # DI 1.x / DO 1.x
  - start_reg: 0
    count: 2
    # LED 1.x
  - start_reg: 20
    count: 1
    # DI 2.x / RO 2.x
  - start_reg: 100
    count: 2
    # DI 3.x / RO 3.x
  - start_reg: 200
    count: 2
modbus_features:
  - feature_type: DI
    count: 4
    major_group: 1
    val_reg: 0
  - feature_type: DO
    count: 4
    major_group: 1
    val_reg: 1
    val_coil: 0
  - feature_type: LED
    major_group: 1
    count: 4
    val_coil: 8
    val_reg: 20
  - feature_type: DI
    count: 16
    major_group: 2
    val_reg: 100
  - feature_type: RO
    major_group: 2
    count: 14
    val_reg: 101
    val_coil: 100
  - feature_type: DI
    count: 16
    major_group: 3
    val_reg: 200
  - feature_type: RO
    major_group: 3
    count: 14
    val_reg: 201
    val_coil: 200
"""

HARDWARE_DATA_IS_LIST: Final[
    str
] = """- start_reg: 0
  count: 2
- start_reg: 20
  count: 1
- start_reg: 100
  count: 2
- start_reg: 200
  count: 2
"""

HARDWARE_DATA_IS_INVALID_YAML: Final[str] = """modbus_features: INVALID:"""

EXTENSION_HARDWARE_DATA_INVALID_KEY: Final[
    str
] = """manufacturer: Eastron
model: SDM120M
modbus_register_block:
  # Voltage
  - start_reg: 0
    count: 2
modbus_features:
  - feature_type: METER
    friendly_name: Voltage
    device_class: voltage
    state_class: measurement
    unit_of_measurement: V
    val_reg: 0
    count: 2
"""

EXTENSION_HARDWARE_DATA_IS_LIST: Final[
    str
] = """- start_reg: 0
  count: 2
"""

EXTENSION_HARDWARE_DATA_IS_INVALID_YAML: Final[str] = """manufacturer: INVALID:"""
