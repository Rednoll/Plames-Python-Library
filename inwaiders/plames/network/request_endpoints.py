from inwaiders.plames.network.input_packets import JavaInputPacket
from inwaiders.plames.network.output_packets import JavaOutputPacket
from inwaiders.plames.network import buffer_utils, plames_client
from inwaiders.plames import plames
from inwaiders.plames import mutable_data


class RequestEndpoint(JavaInputPacket, JavaOutputPacket):

    def __init__(self):
        super().__init__()
        self.request_id = -1

    def on_received(self):
        pass


class AgentIdRequest(RequestEndpoint):

    def __init__(self):
        super().__init__()

    def read(self, input):
        pass

    def write(self, output):
        buffer_utils.write_long(output, mutable_data.agent_id)

    def get_id(self):
        return 2


mutable_data.input_packet_registry.update({2: lambda: AgentIdRequest()})


class MessengerCommandsRequest(RequestEndpoint):

    def __init__(self):
        super().__init__()

    def read(self, input):
        pass

    def write(self, output):

        buffer_utils.write_dict(output, mutable_data.commands_roots_registry, self.session)
        pass

    def get_id(self):
        return 8


mutable_data.input_packet_registry.update({8: lambda: MessengerCommandsRequest()})


class RunObjectMethod(JavaInputPacket):

    def read(self, input):
        self.entity_id = buffer_utils.read_long(input)
        self.target_s_id = buffer_utils.read_int(input)
        self.method_id = buffer_utils.read_long(input)
        self.args = buffer_utils.read_list(input, self.session)

    def on_received(self):

        def run(entity_id=self.entity_id, target_s_id=self.target_s_id, method_id=self.method_id, args=self.args):
            plames.add_hyper_task(run)
