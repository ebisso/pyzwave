"""
pyzwave client example program
"""
import pyzwave

def main():
    """ main function """
    print("pyzwave client")

    class Receiver:
        def on_central_scene_notification(self,
                                          node,
                                          sequence_number,
                                          slow_refresh,
                                          key_attribute,
                                          scene_number):
            info = dict()
            info['node'] = node
            info['sequence_number'] = sequence_number
            info['slow_refresh'] = slow_refresh
            info['key_attribyte'] = key_attribute
            info['scene_number'] = scene_number
            print("Central Scene Notification: " + repr(info))

        def on_switch_binary_report(self, node, value):
            info = dict()
            info['node'] = node
            info['value'] = value
            print("Switch Binary Report: " + repr(info))

        def on_switch_multilevel_report(self, node, value):
            info = dict()
            info['node'] = node
            info['value'] = value
            print("Switch Multilevel Report: " + repr(info))

    controller = pyzwave.Controller()
    controller.set_receiver(Receiver())
    controller.open("COM3")

    try:
        print("Usage:")
        print(" 'switch_binary_get <NODE>'")
        print(" 'switch_binary_set <NODE> <VALUE>'")
        print(" 'switch_multilevel_get <NODE>'")
        print(" 'switch_multilevel_set <NODE> <VALUE>'")
        print(" 'q' : quit")
        print("Examples:")
        print(" 'switch_binary_set 5 255'")
        while True:
            try:
                tokens = input().split()
            except KeyboardInterrupt:
                break
            command = tokens[0]
            if command == "switch_binary_get":
                controller.switch_binary_get(int(tokens[1]))
            elif command == "switch_binary_set":
                controller.switch_binary_set(int(tokens[1]), int(tokens[2]))
            elif command == "switch_multilevel_get":
                controller.switch_multilevel_get(int(tokens[1]))
            elif command == "switch_multilevel_set":
                controller.switch_multilevel_set(int(tokens[1]), int(tokens[2]))
            elif command == "q":
                break
            
    finally:
        controller.close()

if __name__ == "__main__":
    main()
