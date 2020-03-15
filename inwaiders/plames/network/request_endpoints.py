from inwaiders.plames.network.input_packets import JavaInputPacket
from inwaiders.plames.network.output_packets import JavaOutputPacket
from inwaiders.plames.network import buffer_utils, plames_client
from inwaiders.plames import plames
from inwaiders.plames import mutable_data


class RequestEndpoint(JavaInputPacket, JavaOutputPacket):

    def __init__(self):
        super().__init__()
        self.request_id = -1
        self.asynchronous = False

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

    def get_id(self):
        return 8


mutable_data.input_packet_registry.update({8: lambda: MessengerCommandsRequest()})


class RunObjectMethod(RequestEndpoint):

    def read(self, input):
        self.method_id = buffer_utils.read_long(input)
        self.args = buffer_utils.read_list(input, self.session)
        self.asynchronous = True

    def on_received(self):

        def run(request_id=self.request_id, method_id=self.method_id, args=self.args):

            method = mutable_data.methods_registry.get(method_id)
            result = method(args)

            answer = RunObjectMethod()
            answer.request_id = request_id
            answer.result = result

            plames_client.send(answer)

        plames.add_hyper_task(run)

    def write(self, output):
        buffer_utils.write_data(output, self.result, self.session)

    def get_id(self):
        return 20


mutable_data.input_packet_registry.update({20: lambda: RunObjectMethod()})
