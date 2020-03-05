from inwaiders.plames.network import buffer_utils
from inwaiders.plames import plames, mutable_data

class JavaOutputPacket(object):

    def __init__(self):
        self._cached_output = None

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
        buffer_utils.write_entity(output, self.entity, self.session)

        dependencies = self.session.build_dependencies_map(self.entity, True)

        buffer_utils.write_int(output, len(dependencies))

        for dep in dependencies:

            buffer_utils.write_int(output, dep._s_id)
            buffer_utils.write_fields(output, dep, True, self.session)

        del self.entity

    def get_id(self):
        return 7


class BootLoaded(JavaOutputPacket):

    def get_id(self):
        return 11
