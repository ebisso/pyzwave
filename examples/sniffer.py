"""
pyzwave sniffer example program
"""
import pyzwave

def main():
    """ main function """
    print("pyzwave sniffer")

    def _on_dataframe_received(dataframe):
        print("Received: " + repr(dataframe))

    controller = pyzwave.SerialInterface("COM3")
    controller.set_dataframe_received_callback(_on_dataframe_received)
    controller.start()

    try:
        while True:
            try:
                print("Enter 'q' to quit")
                command = input()
            except KeyboardInterrupt:
                break
            if command == "q":
                break
    finally:
        controller.stop()

if __name__ == "__main__":
    main()
