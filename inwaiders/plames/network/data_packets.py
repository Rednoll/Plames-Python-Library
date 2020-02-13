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

class RequestEntity(DataPacket):

    request_id = None

    entity_name = None
    args = None
    method_name = None
    rep_args = None

    def __init__(self, request_id, entity_name, method_name, args, rep_args):
        self.request_id = request_id
        self.entity_name = entity_name
        self.method_name = method_name
        self.args = args if args is not None else []
        self.rep_args = rep_args if rep_args is not None else []

    def write(self, output):
        buffer_utils.write_long(output, self.request_id)
        buffer_utils.write_utf8(output, self.entity_name)
        buffer_utils.write_utf8(output, self.method_name)
        buffer_utils.write_list(output, self.args)
        buffer_utils.write_list(output, self.rep_args)

    def get_id(self):
        return 2