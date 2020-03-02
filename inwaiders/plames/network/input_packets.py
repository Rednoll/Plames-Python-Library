from inwaiders.plames.network import buffer_utils
from inwaiders.plames.network import plames_client
from inwaiders.plames import plames
from inwaiders.plames import mutable_data
from inwaiders.plames.command import command_registry

class JavaInputPacket(object):

    def __init__(self):
        self.session = mutable_data.current_session
        self._cached_input = None

    def read(self, input_socket):
        pass

    def on_received(self):
        pass


class Unlock(JavaInputPacket):

    request_id = None

    def read(self, input_socket):
        self.request_id = buffer_utils.read_long(input_socket)

    def on_received(self):
        plames_client.request_events_dict.get(self.request_id).set()


mutable_data.input_packet_registry.update({1: lambda: Unlock()})


class AgentId(JavaInputPacket):

    def read(self, input):
        self.agent_id = buffer_utils.read_long(input)

    def on_received(self):
        mutable_data.agent_id = self.agent_id


mutable_data.input_packet_registry.update({3: lambda: AgentId()})


class ConnectionInited(JavaInputPacket):

    def read(self, input):
        pass

    def on_received(self):
        mutable_data.plames_connection_inited = True
        
        if mutable_data.connect_lock is not None:
            mutable_data.connect_lock.set()


mutable_data.input_packet_registry.update({10: lambda: ConnectionInited()})


class RunCommand(JavaInputPacket):

    def read(self, input):
        self.command_id = buffer_utils.read_short(input)
        self.profile = buffer_utils.read_entity(input, self.session)
        self.args = buffer_utils.read_string_array(input)

    def on_received(self):
        command = command_registry.get_command(self.command_id)
        command.run(self.profile, self.args)


mutable_data.input_packet_registry.update({12: lambda: RunCommand()})
