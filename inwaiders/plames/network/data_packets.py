import struct
import time
from plistlib import Data
from inwaiders.plames.network import buffer_utils

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

class RequestObject(DataPacket):

    class_name = None
    args = None

    def __init__(self, class_name, args):
        self.class_name = class_name
        self.args = args

    def write(self, output):
        buffer_utils.write_utf8(output, self.class_name)
        buffer_utils.write_list(output, self.args)

    def get_id(self):
        return 2