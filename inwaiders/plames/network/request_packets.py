from inwaiders.plames.network.input_packets import JavaInputPacket
from inwaiders.plames.network.output_packets import JavaOutputPacket
from inwaiders.plames.network import buffer_utils, plames_client
from inwaiders.plames import plames
from inwaiders.plames import mutable_data


class JavaRequest(JavaInputPacket, JavaOutputPacket):

    def __init__(self):
        self.request_id = -1

    def on_received(self):
        pass


class RequestEntity(JavaRequest):

    def __init__(self, entity_name=None, method_name=None, args=None, rep_args=None):
        super().__init__()
        self.entity_name = entity_name
        self.method_name = method_name
        self.args = args if args is not None else []
        self.rep_args = rep_args if rep_args is not None else []
        self.java_object = None

    def write(self, output):
        buffer_utils.write_utf8(output, self.entity_name)
        buffer_utils.write_utf8(output, self.method_name)
        buffer_utils.write_list(output, self.args)
        buffer_utils.write_list(output, self.rep_args)

    def read(self, input_stream):
        self.java_object = buffer_utils.read_data(input_stream, self.session)

    def get_id(self):
        return 0


mutable_data.input_packet_registry.update({0: lambda: RequestEntity()})


class RequestEntityAttr(JavaRequest):

    def __init__(self, s_id=None, field_name=None):
        super().__init__()
        self.s_id = s_id
        self.field_name = field_name

    def write(self, output):
        buffer_utils.write_int(output, self.s_id)
        buffer_utils.write_utf8(output, self.field_name)

    def read(self, input_socket):
        self.java_object = buffer_utils.read_data(input_socket, self.session)

    def get_id(self):
        return 5


mutable_data.input_packet_registry.update({5: lambda: RequestEntityAttr()})


class RequestCreateEntity(JavaRequest):

    def __init__(self, entity_name, args, rep_args):
        super().__init__()
        self.entity_name = entity_name
        self.args = args if args is not None else []
        self.rep_args = rep_args if rep_args is not None else []

    def write(self, output):
        buffer_utils.write_utf8(output, self.entity_name)
        buffer_utils.write_list(output, self.args)
        buffer_utils.write_list(output, self.rep_args)

    def read(self, input_socket):
        self.java_object = buffer_utils.read_data(input_socket, self.session)

    def get_id(self):
        return 6


mutable_data.input_packet_registry.update({6: lambda: RequestCreateEntity()})


class ClassTypesRequest(JavaRequest):

    def __init__(self, name=None):
        super().__init__()
        self.name = name
        self.types = None

    def write(self, output):
        buffer_utils.write_utf8(output, self.name)

    def read(self, input_socket):
        self.types = buffer_utils.read_dict(input_socket, self.session)

    def get_id(self):
        return 9


mutable_data.input_packet_registry.update({9: lambda: ClassTypesRequest()})


class RunMethodRequest(JavaRequest):

    def __init__(self, s_id=None, method_name=None, args=None):
        super().__init__()
        self.s_id = s_id
        self.method_name = method_name
        self.args = args
        self.result = None

    def write(self, output):
        buffer_utils.write_int(output, self.s_id)
        buffer_utils.write_utf8(output, self.method_name)
        buffer_utils.write_list(output, self.args, self.session)

        del self.args

    def read(self, input):
        self.result = buffer_utils.read_data(input, self.session)

    def get_id(self):
        return 13


mutable_data.input_packet_registry.update({13: lambda: RunMethodRequest()})


class RequestStatic(JavaRequest):

    def __init__(self, static_name=None):
        super().__init__()
        self.static_name = static_name
        self.static = None

    def write(self, output):
        buffer_utils.write_utf8(output, self.static_name)

    def read(self, input):
        self.static = buffer_utils.read_data(input, self.session)

    def get_id(self):
        return 14


mutable_data.input_packet_registry.update({14: lambda: RequestStatic()})

