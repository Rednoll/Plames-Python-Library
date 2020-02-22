from inwaiders.plames.network.input_packets import JavaInputPacket, answers
from inwaiders.plames.network.output_packets import JavaOutputPacket
from inwaiders.plames.network import buffer_utils
import sys
from inwaiders.plames import plames
from inwaiders.plames import mutable_data


class JavaRequest(JavaInputPacket, JavaOutputPacket):

    def on_received(self):
        pass


class AgentIdRequest(JavaRequest):

    def write(self, output):
        buffer_utils.write_long(output, mutable_data.agent_id)

    def read(self, input):
        pass

    def get_id(self):
        return 2


answers.update({2: lambda: AgentIdRequest()})


class MessengerCommandsRequest(JavaRequest):

    def write(self, output):

        buffer_utils.write_dict(output, mutable_data.commands_registry)
        pass

    def read(self, input):
        pass

    def get_id(self):
        return 8


answers.update({2: lambda: MessengerCommandsRequest()})
