import socket
import struct
import time
from inwaiders.plames.network import buffer_utils
from inwaiders.plames.network import plames_client
import sys
from inwaiders.plames.network import output_packets
from inwaiders.plames import plames
from inwaiders.plames import mutable_data
answers = {}


class JavaInputPacket(object):

    def __init__(self):
        self.session = plames.Session()

    def read(self, input_socket):
        pass

    def on_received(self):
        pass


class RequestEntity(JavaInputPacket):

    java_object = None

    def __init__(self):
        self.request_id = None

    def read(self, input_socket):
        self.request_id = buffer_utils.read_long(input_socket)
        self.java_object = buffer_utils.read_data(input_socket, self.session)

    def on_received(self):
        plames_client.request_data_dict.update({self.request_id: self.java_object})
        plames_client.request_events_dict.get(self.request_id).set()


answers.update({0: lambda: RequestEntity()})


class Unlock(JavaInputPacket):

    request_id = None

    def read(self, input_socket):
        self.request_id = buffer_utils.read_long(input_socket)

    def on_received(self):
        plames_client.request_events_dict.get(self.request_id).set()


answers.update({1: lambda: Unlock()})


class AgentId(JavaInputPacket):

    def read(self, input):
        self.agent_id = buffer_utils.read_long(input)

    def on_received(self):
        mutable_data.agent_id = self.agent_id


answers.update({3: lambda: AgentId()})
