"""
pyzwave sniffer example program
"""
import pyzwave

def main():
    """ main function """
    print("pyzwave sniffer")

    def _on_dataframe_received(dataframe):
        info = dict()
        info['prefix'] = dataframe[0]
        info['length'] = dataframe[1]
        info['type'] = dataframe[2]
        info['api_command'] = dataframe[3]
        info['data'] = dataframe[4:len(dataframe) - 5]
        info['checksum'] = dataframe[len(dataframe) - 1]
        print("Received: " + repr(dataframe) + "    " + repr(info))

    interface = pyzwave.SerialInterface("COM3")
    interface.set_dataframe_received_callback(_on_dataframe_received)
    interface.start()

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
        interface.stop()

if __name__ == "__main__":
    main()
