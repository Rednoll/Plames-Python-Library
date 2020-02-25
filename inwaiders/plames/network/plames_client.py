import socket
import struct
import threading
from threading import Lock, Event
from multiprocessing import Queue

from inwaiders.plames.plames import mutable_data
from inwaiders.plames.network.request_packets import JavaRequest
from inwaiders.plames.network.request_endpoints import RequestEndpoint
from inwaiders.plames.network import output_packets
from inwaiders.plames.network import buffer_utils
import logging

logger = logging.getLogger("Plames.Plames-Client")

clientSocket = None
packetsQueue = Queue()
sender = None
listener = None

next_request_id = 0

request_id_lock = Lock()
request_events_dict = {}
request_data_dict = {}

connect_lock = None

def connect(address, port, lock=True):
    global clientSocket, sender, listener, connect_lock

    connect_lock = Event()

    clientSocket = socket.socket()
    clientSocket.connect((address, port))

    sender = threading.Thread(target=__write_packets)
    sender.start()

    listener = threading.Thread(target=__listen)
    listener.start();

    connect_lock.wait()



def send(packet):
    global packetsQueue
    packet._cached_output = []
    packet.write(packet._cached_output)
    packetsQueue.put(packet)


def create(entity_name, args=[], rep_args=[]):
    global next_request_id, request_events_dict, request_data_dict

    request_id = -1

    with request_id_lock:
        request_id = next_request_id
        next_request_id += 1

    event = Event()
    request_events_dict.update({request_id: event})

    send(output_packets.RequestCreateEntity(request_id, entity_name, args, rep_args))

    event.wait()

    return request_data_dict.get(request_id)


def request(request_packet):
    global next_request_id, request_events_dict, request_data_dict

    request_id = -1

    with request_id_lock:
        request_id = next_request_id
        next_request_id += 1

    event = Event()
    request_events_dict.update({request_id: event})

    request_packet.request_id = request_id

    send(request_packet)

    event.wait()

    return request_data_dict.get(request_id)


def request_entity(entity_name, method_name, args, rep_args=[]):
    global next_request_id, request_events_dict, request_data_dict

    request_id = -1

    with request_id_lock:
        request_id = next_request_id
        next_request_id += 1

    event = Event()
    request_events_dict.update({request_id: event})

    send(output_packets.RequestEntity(request_id, entity_name, method_name, args, rep_args))

    event.wait()

    return request_data_dict.get(request_id)


def request_attr(entity_name, entity_id, field_name):
    global next_request_id, request_events_dict, request_data_dict

    field_name = buffer_utils.to_camel_case(field_name)

    request_id = -1

    with request_id_lock:
        request_id = next_request_id
        next_request_id += 1

    event = Event()
    request_events_dict.update({request_id: event})

    send(output_packets.RequestEntityAttr(request_id, entity_name, entity_id, field_name))

    event.wait()

    return request_data_dict.get(request_id)


def push(entity, blocking=False):
    global next_request_id, request_events_dict, request_data_dict

    if not blocking:
        send(output_packets.PushEntity(entity))
    else:
        request_id = -1

        with request_id_lock:
            request_id = next_request_id
            next_request_id += 1

        event = Event()
        request_events_dict.update({request_id: event})

        send(output_packets.PushEntity(entity, request_id))

        event.wait()


def __on_disconnect():
    logger.info("Disconnected from Plames machine")
    mutable_data.plames_connection_inited = False


def __write_packets():
    global clientSocket, packetsQueue

    while True:
        '''
        while not mutable_data.plames_connection_inited:
            pass
        '''
        packet = packetsQueue.get(True)

        output = bytearray(packet._cached_output)

        clientSocket.send(struct.pack(">h", packet.get_id()))
        clientSocket.send(struct.pack(">i", len(output)))

        if isinstance(packet, JavaRequest):
            clientSocket.send(struct.pack(">q", packet.request_id))

        clientSocket.send(output)

        del packet._cached_output


def __listen():
    global clientSocket

    try:

        while True:
            packet_id = struct.unpack(">h", clientSocket.recv(2, socket.MSG_WAITALL))[0]
            size = clientSocket.recv(4, socket.MSG_WAITALL)

            packet = mutable_data.input_packet_registry.get(packet_id)()

            if isinstance(packet, JavaRequest) or isinstance(packet, RequestEndpoint):
                packet.request_id = struct.unpack(">q", clientSocket.recv(8, socket.MSG_WAITALL))[0]

            packet.read(clientSocket)
            packet.on_received()

            if isinstance(packet, RequestEndpoint):
                send(packet)

    except ConnectionAbortedError:
        __on_disconnect()



