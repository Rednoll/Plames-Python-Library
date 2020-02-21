from inwaiders.plames.network.java_answer import JavaAnswer, answers
from inwaiders.plames.network.data_packets import DataPacket
from inwaiders.plames.network import buffer_utils
from inwaiders.plames import Plames

class JavaRequest(JavaAnswer, DataPacket):

    def on_received(self):
        pass


class AgentIdJavaRequest(JavaRequest):

    def write(self, output):
        buffer_utils.write_long(output, Plames.agent_id)

    def read(self, input):
        pass

    def get_id(self):
        return 6


answers.update({6: lambda: AgentIdJavaRequest()})
