"""
Controller class
"""

class Controller:

    def __init__(self, serial, serial_reader_thread):
        self.serial = serial
        self.serial_reader_thread = serial_reader_thread
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def start(self):
        def callback(read_bytes):
            if self.callback:
                self.callback(read_bytes)

        self.serial_reader_thread.set_callback(callback)

        self.serial.open()
        self.serial_reader_thread.start()

    def stop(self):
        self.serial_reader_thread.stop()
        self.serial_reader_thread.join()
        self.serial.close()
