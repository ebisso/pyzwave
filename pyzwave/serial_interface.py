"""
pyzwave.serial_interface module
"""
import enum
import queue
import threading
from . import constants, input_stream, serial_wrapper

class SerialInterface:
    """
    This class handles serial communication with the Z-Wave controller
    """
    def __init__(self, device):
        self._callback = None
        self._serial = serial_wrapper.SerialWrapper(device)
        self._msg_queue = queue.Queue()
        self._stop = False
        self._instream = input_stream.InputStream()
        self._read_thread = threading.Thread(target=self._serial_read_loop)
        self._process_thread = threading.Thread(target=self._process_loop)

    def set_callback(self, callback):
        """ set the callback method """
        self._callback = callback

    def start(self):
        """ Opens port and starts processing """
        self._serial.open()
        self._read_thread.start()
        self._process_thread.start()

    def stop(self):
        """ Stops processing and close port """
        self._msg_queue.put(Message.Stop)
        self._process_thread.join()
        self._read_thread.join()
        self._serial.close()

    def _serial_read_loop(self):
        while True:
            if self._stop:
                break
            data = self._serial.read()
            if data:
                self._instream.write(data)
                self._msg_queue.put(Message.Read)

    def _process_loop(self):
        while True:
            msg = self._msg_queue.get()
            if msg == Message.Stop:
                self._stop = True
                break
            elif msg == Message.Read:
                self._read()
            elif msg == Message.Write:
                pass

    def _read(self):
        prefix = self._instream.read(1, 0)
        if prefix:
            if prefix[0] == constants.DATA_FRAME_PREFIX:
                length = self._instream.read(1, 1)
                if length:
                    body = self._instream.read(length[0], 1)
                    if body:
                        dataframe = dict()
                        dataframe['prefix'] = constants.DATA_FRAME_PREFIX
                        dataframe['length'] = length[0]
                        dataframe['type'] = body[0]
                        dataframe['command'] = body[1]
                        dataframe['payload'] = body[2:length[0] - 1]
                        dataframe['checksum'] = body[length[0] - 1]
                        self._write_ack()
                        self._on_data_frame(dataframe)
            elif prefix[0] == constants.ACK_FRAME_PREFIX:
                self._on_ack_frame()
            elif prefix[0] == constants.NAK_FRAME_PREFIX:
                self._on_nak_frame()
            elif prefix[0] == constants.CANCEL_FRAME_PREFIX:
                self._on_cancel_frame()

    def _write_ack(self):
        self._serial.write(bytes([constants.ACK_FRAME_PREFIX]))

    def _on_data_frame(self, dataframe):
        self._callback(str(dataframe))

    def _on_ack_frame(self):
        self._callback("ACK")

    def _on_nak_frame(self):
        self._callback("NAK")

    def _on_cancel_frame(self):
        self._callback("CAN")

class Message(enum.Enum):
    """
    The operations done in the main loop of the controller
    """
    Stop = "Processing needs to stop"
    Read = "Data has been received"
    Write = "Data needs to be sent"
