import socket
import struct
import threading
from threading import Lock, Event
from multiprocessing import Queue

from inwaiders.plames.network import java_answer
from inwaiders.plames.network import data_packets
from inwaiders.plames.network import buffer_utils

clientSocket = None
packetsQueue = Queue()
sender = None
listener = None

next_entity_request_id = 0

request_id_lock = Lock()
request_events_dict = {}
request_data_dict = {}

def connect(address, port):
    global clientSocket, sender, listener

    if clientSocket is not None:
        raise RuntimeError("Клиент уже подключен!")

    clientSocket = socket.socket()
    clientSocket.connect((address, port))

    sender = threading.Thread(target=__write_packets)
    sender.start()

    listener = threading.Thread(target=__listen)
    listener.start();


def send(packet):
    global packetsQueue
    packet._cached_output = []
    packet.write(packet._cached_output)
    packetsQueue.put(packet)


def create(entity_name, args=[], rep_args=[]):
    global next_entity_request_id, request_events_dict, request_data_dict

    request_id = -1

    with request_id_lock:
        request_id = next_entity_request_id
        next_entity_request_id += 1

    event = Event()
    request_events_dict.update({request_id: event})

    send(data_packets.RequestCreateEntity(request_id, entity_name, args, rep_args))

    event.wait()

    return request_data_dict.get(request_id)

def request(entity_name, method_name, args, rep_args=[]):
    global next_entity_request_id, request_events_dict, request_data_dict

    request_id = -1

    with request_id_lock:
        request_id = next_entity_request_id
        next_entity_request_id += 1

    event = Event()
    request_events_dict.update({request_id: event})

    send(data_packets.RequestEntity(request_id, entity_name, method_name, args, rep_args))

    event.wait()

    return request_data_dict.get(request_id)


def request_attr(entity_name, entity_id, field_name):
    global next_entity_request_id, request_events_dict, request_data_dict

    field_name = buffer_utils.to_camel_case(field_name)

    request_id = -1

    with request_id_lock:
        request_id = next_entity_request_id
        next_entity_request_id += 1

    event = Event()
    request_events_dict.update({request_id: event})

    send(data_packets.RequestEntityAttr(request_id, entity_name, entity_id, field_name))

    event.wait()

    return request_data_dict.get(request_id)


def push(entity):
    send(data_packets.PushEntity(entity))


def __write_packets():
    global clientSocket, packetsQueue

    while True:
        packet = packetsQueue.get(True)

        output = bytearray(packet._cached_output)

        clientSocket.send(struct.pack(">h", packet.get_id()))
        clientSocket.send(struct.pack(">i", len(output)))
        clientSocket.send(output)

        del packet._cached_output

def __listen():
    global clientSocket

    while True:
        packet_id = struct.unpack(">h", clientSocket.recv(2, socket.MSG_WAITALL))[0]
        clientSocket.recv(4, socket.MSG_WAITALL)
        packet = java_answer.answers.get(packet_id)()
        packet.read(clientSocket)
        packet.on_received()

