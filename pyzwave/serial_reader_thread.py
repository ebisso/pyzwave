"""
SerialReaderThread class
"""
from threading import Thread

class SerialReaderThread(Thread):
    def __init__(self, serial, stop_event):
        Thread.__init__(self)
        self.serial = serial
        self.stop_event = stop_event
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def stop(self):
        self.stop_event.set()

    def run(self):
        while True:
            if self.stop_event.is_set():
                break
            read_bytes = self.serial.read(self.serial.in_waiting or 1)
            if read_bytes:
                self.callback(read_bytes)
