import socket
import struct
import time
from inwaiders.plames.network import  buffer_utils
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


class ObjectJavaAnswer(JavaAnswer):

    java_object = None

    def read(self, input_socket):
        java_object = buffer_utils.read_object(input_socket)
        print(java_object.__class__.__name__)

    def on_received(self):
        pass