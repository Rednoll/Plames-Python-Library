import socket
import struct
import time
from inwaiders.plames.network import buffer_utils
from inwaiders.plames.network import plames_client
from inwaiders.plames import Plames
import sys
from inwaiders.plames.network import data_packets

answers = {}


class JavaAnswer(object):

    def read(self, input_socket):
        pass

    def on_received(self):
        pass


class HelloJavaAnswer(JavaAnswer):

    data = None

    def read(self, input_socket):
        data_size = struct.unpack(">i", input_socket.recv(4, socket.MSG_WAITALL))[0]
        self.data = input_socket.recv(data_size, socket.MSG_WAITALL).decode("utf-8")

    def on_received(self):
        print(self.data)


answers.update({0: lambda: HelloJavaAnswer()})


class PingJavaAnswer(JavaAnswer):

    time = None;

    def read(self, input_socket):
        self.time = struct.unpack(">Q", input_socket.recv(8, socket.MSG_WAITALL))[0]

    def on_received(self):
        current_time = int(round(time.time() * 1000))
        print("ping: "+str(current_time-self.time))


answers.update({1: lambda: PingJavaAnswer()})


class TestObjectJavaAnswer(JavaAnswer):

    def read(self, input_socket):
        java_object = buffer_utils.read_data(input_socket)

    def on_received(self):
        pass


answers.update({2: lambda: TestObjectJavaAnswer()})


class RequestEntityJavaAnswer(JavaAnswer):

    request_id = None

    java_object = None

    def read(self, input_socket):
        self.request_id = buffer_utils.read_long(input_socket)
        self.java_object = buffer_utils.read_data(input_socket, Plames.Session())

    def on_received(self):
        plames_client.request_data_dict.update({self.request_id: self.java_object})
        plames_client.request_events_dict.get(self.request_id).set()


answers.update({3: lambda: RequestEntityJavaAnswer()})


class UnlockJavaAnswer(JavaAnswer):

    request_id = None

    def read(self, input_socket):
        self.request_id = buffer_utils.read_long(input_socket)

    def on_received(self):
        plames_client.request_events_dict.get(self.request_id).set()


answers.update({4: lambda: UnlockJavaAnswer()})


class AgentIdJavaAnswer(JavaAnswer):

    def read(self, input):
        self.agent_id = buffer_utils.read_long(input)

    def on_received(self):
        Plames.agent_id = self.agent_id


answers.update({5: lambda: AgentIdJavaAnswer()})


class AgentIdJavaAnswer(JavaAnswer):

    def read(self, input):
        self.agent_id = buffer_utils.read_long(input)

    def on_received(self):
        Plames.set_agent_id(self.agent_id)


answers.update({7: lambda: AgentIdJavaAnswer()})
