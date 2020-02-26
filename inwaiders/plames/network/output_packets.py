from inwaiders.plames.network import buffer_utils
from inwaiders.plames import plames


class JavaOutputPacket(object):

    def __init__(self):
        self._cached_output = None
        self.session = plames.Session()

    def write(self, output):
        pass

    def get_id(self):
        pass


class PushEntity(JavaOutputPacket):

    def __init__(self, entity, request_id=-1):
        self.entity = entity
        self.request_id = request_id

    def write(self, output):
        buffer_utils.write_long(output, self.request_id)
        buffer_utils.write_entity(output, self.entity)
        del self.entity

    def get_id(self):
        return 7
