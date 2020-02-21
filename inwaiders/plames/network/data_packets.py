import struct
import time
from plistlib import Data
from inwaiders.plames.network import buffer_utils

class DataPacket(object):

    _cached_output = None

    def write(self, output):
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


class RequestEntityAttr(DataPacket):

    def __init__(self, request_id, entity_name, entity_id, field_name):
        self.request_id = request_id
        self.entity_name = entity_name
        self.entity_id = entity_id
        self.field_name = field_name

    def write(self, output):
        buffer_utils.write_long(output, self.request_id)
        buffer_utils.write_utf8(output, self.entity_name)
        buffer_utils.write_long(output, self.entity_id)
        buffer_utils.write_utf8(output, self.field_name)

    def get_id(self):
        return 3


class RequestCreateEntity(DataPacket):

    def __init__(self, request_id, entity_name, args, rep_args):
        self.request_id = request_id
        self.entity_name = entity_name
        self.args = args if args is not None else []
        self.rep_args = rep_args if rep_args is not None else []

    def write(self, output):
        buffer_utils.write_long(output, self.request_id)
        buffer_utils.write_utf8(output, self.entity_name)
        buffer_utils.write_list(output, self.args)
        buffer_utils.write_list(output, self.rep_args)

    def get_id(self):
        return 4


class PushEntity(DataPacket):

    def __init__(self, entity, request_id=-1):
        self.entity = entity
        self.request_id = request_id

    def write(self, output):
        buffer_utils.write_long(output, self.request_id)
        buffer_utils.write_entity(output, self.entity)
        del self.entity

    def get_id(self):
        return 5
