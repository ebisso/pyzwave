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
        self._dataframe_received_callback = None
        self._serial = serial_wrapper.SerialWrapper(device)
        self._msg_queue = queue.Queue()
        self._current = None # data frame sent not yet acknowledged
        self._queued = queue.Queue() # data frames to send
        self._stop = False
        self._instream = input_stream.InputStream()
        self._read_thread = threading.Thread(target=self._serial_read_loop)
        self._process_thread = threading.Thread(target=self._process_loop)

    def set_dataframe_received_callback(self, callback):
        """ set the callback method """
        self._dataframe_received_callback = callback

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

    def send(self, dataframe):
        """ Sends a dataframe """
        self._queued.put(dataframe)
        self._msg_queue.put(Message.Write)

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
                self._write_next()

    def _read(self):
        prefix = self._instream.read_one(0)
        if prefix:
            if prefix == constants.DATA_FRAME_PREFIX:
                self._on_data_frame()
            elif prefix == constants.ACK_FRAME:
                self._on_ack_frame()
            elif prefix == constants.NAK_FRAME:
                self._on_nak_frame()
            elif prefix[0] == constants.CANCEL_FRAME:
                self._on_cancel_frame()

    def _on_data_frame(self):
        length = self._instream.read_one(1)
        if length:
            body = self._instream.read(length, 1)
            if body:
                dataframe = dict()
                dataframe['prefix'] = constants.DATA_FRAME_PREFIX
                dataframe['length'] = length
                dataframe['type'] = body[0]
                dataframe['command'] = body[1]
                dataframe['payload'] = body[2:length - 1]
                dataframe['checksum'] = body[length - 1]
                self._write_ack()
                self._dataframe_received_callback(dataframe)

    def _on_ack_frame(self):
        self._current = None
        self._write_next()

    def _on_nak_frame(self):
        self._serial.write(self._current)

    def _on_cancel_frame(self):
        self._serial.write(self._current)

    def _write_ack(self):
        self._serial.write(bytes([constants.ACK_FRAME]))

    def _write_next(self):
        if self._current:
            return
        if self._queued.empty():
            return
        self._current = self._queued.get()
        self._serial.write(self._current)

class Message(enum.Enum):
    """
    The operations done in the main loop of the controller
    """
    Stop = 0
    Read = 1
    Write = 2
