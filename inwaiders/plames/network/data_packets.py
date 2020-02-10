import struct
import time

class DataPacket(object):

    def write(self):
        pass

    def get_id(self):
        pass

class HelloJavaPacket(DataPacket):

    def write(self, output):
        rawArray = "Hello Java!".encode("utf-8")
        output.extend(struct.pack(">i", len(rawArray)))
        output.extend(rawArray)

    def get_id(self):
        return 0

class PingJavaPacket(DataPacket):

    def write(self, output):
        output.extend(struct.pack(">q", int(round(time.time() * 1000))))

    def get_id(self):
         return 1
