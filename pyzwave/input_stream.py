"""
pyzwave.input_stream module
"""
import threading

class InputStream:
    """
    This class handles a stream of bytes for producer-consumer usage
    """
    def __init__(self):
        self._data = bytearray()
        self._cv = threading.Condition()
        self._treshold = 0

    def read(self, count, timeout):
        """ Reads the specified number of bytes from the stream """
        with self._cv:
            if len(self._data) >= count:
                # data is already available
                result = self._data[0:count]
                del self._data[0:count]
                return result
            else:
                # await data
                self._treshold = count
                self._cv.wait(timeout)
                if len(self._data) >= count:
                    result = self._data[0:count]
                    del self._data[0:count]
                    return result

        return None

    def read_one(self, timeout):
        """ Reads a single byte from the stream """
        result = self.read(1, timeout)
        if result:
            return result[0]

    def write(self, data):
        """ Writes to the stream """
        with self._cv:
            self._data.extend(data)
            if len(self._data) >= self._treshold:
                self._cv.notify()
