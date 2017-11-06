""" controller module """
from . import serial_interface, constants

class Controller:
    """ Controller class """
    def __init__(self):
        self._serial = None
        self._receiver = None

    def open(self, device):
        self._serial = serial_interface.SerialInterface(device)
        self._serial.set_dataframe_received_callback(self._on_dataframe_received)
        self._serial.start()

    def close(self):
        self._serial.stop()

    def send_command(self, node, command_class, command, values):
        dataframe = bytearray()
        dataframe.append(constants.DATA_FRAME_PREFIX)
        dataframe.append(9 + len(values))
        dataframe.append(constants.DATA_FRAME_TYPE_REQUEST)
        dataframe.append(constants.DATA_FRAME_API_COMMAND_SEND_DATA)
        dataframe.append(node)
        dataframe.append(2 + len(values))
        dataframe.append(command_class)
        dataframe.append(command)
        for val in values:
            dataframe.append(val)
        dataframe.append(0)
        dataframe.append(1)
        checksum = 0xFF ^ dataframe[0]
        for byte in dataframe:
            checksum = checksum ^ byte
        dataframe.append(checksum & 0xFF)
        self._serial.send(dataframe)

    def set_receiver(self, receiver):
        self._receiver = receiver

    def switch_binary_get(self, node):
        self.send_command(node,
                          constants.COMMAND_CLASS_SWITCH_BINARY,
                          constants.SWITCH_BINARY_GET,
                          bytes())

    def switch_binary_set(self, node, value):
        self.send_command(node,
                          constants.COMMAND_CLASS_SWITCH_BINARY,
                          constants.SWITCH_BINARY_SET,
                          bytes([value]))

    def switch_multilevel_get(self, node):
        self.send_command(node,
                          constants.COMMAND_CLASS_SWITCH_MULTILEVEL,
                          constants.SWITCH_MULTILEVEL_GET,
                          bytes())

    def switch_multilevel_set(self, node, value):
        self.send_command(node,
                          constants.COMMAND_CLASS_SWITCH_MULTILEVEL,
                          constants.SWITCH_MULTILEVEL_SET,
                          bytes([value]))

    def _on_dataframe_received(self, dataframe):
        dataframe_api_command = dataframe[3]
        if dataframe_api_command == constants.DATA_FRAME_API_COMMAND_APPLICATION_COMMAND:
            node = dataframe[5]
            command_class = dataframe[7]
            command = dataframe[8]
            if command_class == constants.COMMAND_CLASS_CENTRAL_SCENE:
                if command == constants.CENTRAL_SCENE_NOTIFICATION:
                    sequence_number = dataframe[9]
                    slow_refresh = dataframe[10] & 0x80
                    key_attribute = dataframe[10] & 0x07
                    scene_number = dataframe[11]
                    self._receiver.on_central_scene_notification(node,
                                                                 sequence_number,
                                                                 slow_refresh,
                                                                 key_attribute,
                                                                 scene_number)
            elif command_class == constants.COMMAND_CLASS_SWITCH_BINARY:
                if command == constants.SWITCH_BINARY_REPORT:
                    value = dataframe[9]
                    self._receiver.on_switch_binary_report(node, value)
            elif command_class == constants.COMMAND_CLASS_SWITCH_MULTILEVEL:
                if command == constants.SWITCH_MULTILEVEL_REPORT:
                    value = dataframe[9]
                    self._receiver.on_switch_multilevel_report(node, value)
