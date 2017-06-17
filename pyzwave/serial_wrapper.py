"""
pyzwave.serial_wrapper module
"""
import serial

class SerialWrapper:
    """
    This class wraps a Serial instance and handles the serial port initialization
    """

    def __init__(self, device):
        self.serial = serial.Serial()
        self.serial.baudrate = 115200
        self.serial.port = device
        self.serial.timeout = 3

    def open(self):
        """ Opens the serial port """
        self.serial.open()

    def close(self):
        """ Closes the serial port """
        self.serial.close()

    def read(self):
        """ Reads as much bytes as possible from the serial port """
        return self.serial.read(self.serial.in_waiting or 1)

    def write(self, data):
        """ Writes bytes to the serial port """
        self.serial.write(data)
