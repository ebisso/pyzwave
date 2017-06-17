"""
pyzwave sniffer example program
"""
import pyzwave

def main():
    """ main function """
    print("pyzwave sniffer")

    def _callback(message):
        print("Message: " + message)

    controller = pyzwave.SerialInterface("COM3")
    controller.set_callback(_callback)
    controller.start()

    try:
        while True:
            try:
                command = input("Enter 'q' to quit:")
            except KeyboardInterrupt:
                break
            if command == "q":
                break
    finally:
        controller.stop()

if __name__ == "__main__":
    main()
