from inwaiders.plames.network.input_packets import JavaInputPacket
from inwaiders.plames.network.output_packets import JavaOutputPacket
from inwaiders.plames.network import buffer_utils, plames_client
from inwaiders.plames import plames
from inwaiders.plames import mutable_data


class JavaRequest(JavaInputPacket, JavaOutputPacket):

    def __init__(self):
        self.session = plames.Session()
        self.request_id = -1

    def on_received(self):
        plames_client.request_data_dict.update({self.request_id: self})
        plames_client.request_events_dict.get(self.request_id).set()


class ClassTypesRequest(JavaRequest):

    def __init__(self, name=None):
        self.name = name
        self.types = None

    def write(self, output):
        buffer_utils.write_utf8(output, self.name)

    def read(self, input):
        self.types = buffer_utils.read_dict(input=input, session=self.session)

    def get_id(self):
        return 9


mutable_data.input_packet_registry.update({9: lambda: ClassTypesRequest()})
