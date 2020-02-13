import socket
import struct
import threading
from threading import Lock, Event
from multiprocessing import Queue

from inwaiders.plames.network import java_answer
from inwaiders.plames.network import data_packets

clientSocket = None
packetsQueue = Queue()
sender = None
listener = None

next_entity_request_id = 0

entity_request_id_lock = Lock()
entity_request_events_dict = {}
entity_request_data_dict = {}

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
    packetsQueue.put(packet)


def request(entity_name, method_name, args, rep_args=[]):
    global next_entity_request_id, entity_request_events_dict, entity_request_data_dict

    request_id = -1

    with entity_request_id_lock:
        request_id = next_entity_request_id
        next_entity_request_id += 1

    event = Event()
    entity_request_events_dict.update({request_id: event})

    send(data_packets.RequestEntity(request_id, entity_name, method_name, args, rep_args))

    event.wait()

    return entity_request_data_dict.get(request_id)

def __write_packets():
    global clientSocket, packetsQueue

    while True:
        packet = packetsQueue.get(True)

        output = []
        packet.write(output)

        clientSocket.send(struct.pack(">h", packet.get_id()))
        clientSocket.send(struct.pack(">i", len(output)))
        clientSocket.send(bytearray(output))


def __listen():
    global clientSocket

    while True:
        packet_id = struct.unpack(">h", clientSocket.recv(2, socket.MSG_WAITALL))[0]
        clientSocket.recv(4, socket.MSG_WAITALL)
        packet = java_answer.answers.get(packet_id)()
        packet.read(clientSocket)
        packet.on_received()
