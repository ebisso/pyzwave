"""
pyzwave.constants module

Constants for the Z-Wave protocol
"""
# Serial frame types.
DATA_FRAME_PREFIX = 0x01   # Data frame
ACK_FRAME_PREFIX = 0x06    # ACK frame
NAK_FRAME_PREFIX = 0x15    # NAK frame
CANCEL_FRAME_PREFIX = 0x18 # Cancel frame

# Data frame types
DATA_FRAME_TYPE_REQUEST = 0x00
DATA_FRAME_TYPE_RESPONSE = 0x01

# Data frame commands (incomplete)
DATA_FRAME_COMMAND_APPLICATION_COMMAND_HANDLER = 0x04
DATA_FRAME_COMMAND_ZW_GET_VERSION = 0x15
DATA_FRAME_COMMAND_APPLICATION_NODEINFO = 0x03
