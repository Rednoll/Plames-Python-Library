from inwaiders.plames.network import buffer_utils
from inwaiders.plames.network import plames_client
from inwaiders.plames import plames
from inwaiders.plames import mutable_data
from inwaiders.plames.command import command_registry

class JavaInputPacket(object):

    def __init__(self):
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
        mutable_data.request_events_dict.get(self.request_id).set()


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


class RunMessengerCommand(JavaInputPacket):

    def read(self, input):
        self.command_id = buffer_utils.read_short(input)
        self.profile_link = buffer_utils.read_entity_link(input, self.session)
        self.args = buffer_utils.read_string_array(input)

    def on_received(self):

        command = command_registry.get_command(self.command_id)

        def run(command=command, profile_link=self.profile_link, args=self.args):

            profile = plames_client.request_entity(link=profile_link)

            command.run(profile, args)

        plames.add_hyper_task(run)


mutable_data.input_packet_registry.update({12: lambda: RunMessengerCommand()})
