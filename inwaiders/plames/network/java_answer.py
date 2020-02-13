import socket
import struct
import time
from inwaiders.plames.network import buffer_utils
from inwaiders.plames.network import plames_client
import sys

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
        java_object = buffer_utils.read_object(input_socket)

    def on_received(self):
        pass


answers.update({2: lambda: TestObjectJavaAnswer()})


class RequestEntityJavaAnswer(JavaAnswer):

    request_id = None

    java_object = None

    def read(self, input_socket):
        self.request_id = buffer_utils.read_long(input_socket)
        self.java_object = buffer_utils.read_object(input_socket)

    def on_received(self):
        plames_client.entity_request_data_dict.update({self.request_id: self.java_object})
        plames_client.entity_request_events_dict.get(self.request_id).set()


answers.update({3: lambda: RequestEntityJavaAnswer()})
