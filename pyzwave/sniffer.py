"""
Sniffer
"""

from controller import Controller
from serial import Serial
from serial_reader_thread import SerialReaderThread
from threading import Event
from binascii import unhexlify

def main():
    print("pyzwave sniffer")

    serial = Serial()
    serial.port = "COM3"
    serial.baudrate = 115200
    serial.timeout = 3

    stop_event = Event()

    serial_reader_thread = SerialReaderThread(serial, stop_event)

    def callback(message):
        print("Message: "+message.hex())

    controller = Controller(serial, serial_reader_thread)
    controller.set_callback(callback)
    controller.start()

    try:
        while True:
            try:
                command = input("Enter q to quit:")
                if command == "q":
                    break
            except KeyboardInterrupt:
                break
    finally:
        controller.stop()

if __name__ == "__main__":
    main()
