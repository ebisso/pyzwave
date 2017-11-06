"""
pyzwave.constants module

Constants for the Z-Wave protocol
"""
# Serial frame types.
DATA_FRAME_PREFIX = 0x01   # Data frame
ACK_FRAME = 0x06           # ACK frame
NAK_FRAME = 0x15           # NAK frame
CANCEL_FRAME = 0x18        # Cancel frame

# Data frame types
DATA_FRAME_TYPE_REQUEST = 0x00
DATA_FRAME_TYPE_RESPONSE = 0x01

# Data frame commands (incomplete)
DATA_FRAME_API_COMMAND_APPLICATION_COMMAND = 0x04
DATA_FRAME_API_COMMAND_SEND_DATA = 0x13

# Command classes
COMMAND_CLASS_SWITCH_BINARY = 0x25
COMMAND_CLASS_SWITCH_MULTILEVEL = 0x26
COMMAND_CLASS_CENTRAL_SCENE = 0x5B

# Switch binary commands
SWITCH_BINARY_SET = 0x01
SWITCH_BINARY_GET = 0x02
SWITCH_BINARY_REPORT = 0x03

# Switch multilevel commands
SWITCH_MULTILEVEL_SET = 0x01
SWITCH_MULTILEVEL_GET = 0x02
SWITCH_MULTILEVEL_REPORT = 0x03

# Central scene commands
CENTRAL_SCENE_NOTIFICATION = 0x03
