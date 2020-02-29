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
from inwaiders.plames.network import request_packets
import logging
from io import BytesIO

logger = logging.getLogger("Plames.Plames-Client")


def connect(address, port, lock=True):

    if lock:
        mutable_data.connect_lock = Event()

    mutable_data.clientSocket = socket.socket()
    mutable_data.clientSocket.connect((address, port))

    mutable_data.sender = threading.Thread(target=__write_packets)
    mutable_data.sender.start()

    mutable_data.listener = threading.Thread(target=__listen)
    mutable_data.listener.start()

    mutable_data.executor = threading.Thread(target=__execute_func)
    mutable_data.executor.start()

    if lock:
        mutable_data.connect_lock.wait()


def send(packet):
    packet._cached_output = BytesIO()
    packet.write(packet._cached_output)
    mutable_data.packetsQueue.put(packet)


def create(entity_name, args=[], rep_args=[]):
    return request(request_packets.RequestCreateEntity(entity_name, args, rep_args)).java_object


def request(request_packet):

    mutable_data.request_id_lock.acquire()

    request_id = mutable_data.next_request_id
    mutable_data.next_request_id += 1

    mutable_data.request_id_lock.release()

    event = Event()
    mutable_data.request_events_dict.update({request_id: event})

    request_packet.request_id = request_id

    send(request_packet)

    event.wait()

    answer_packet = mutable_data.request_data_dict.get(request_id)

    __execute(answer_packet)

    return answer_packet


def request_entity(entity_name, method_name, args, rep_args=[]):
    return request(request_packets.RequestEntity(entity_name, method_name, args, rep_args)).java_object


def request_attr(entity_name, entity_id, field_name):
    return request(request_packets.RequestEntityAttr(entity_name, entity_id, field_name)).java_object


def push(entity, blocking=False):

    if not blocking:
        send(output_packets.PushEntity(entity))
    else:
        request_id = -1

        with mutable_data.request_id_lock:
            request_id = mutable_data.next_request_id
            mutable_data.next_request_id += 1

        event = Event()
        mutable_data.request_events_dict.update({request_id: event})

        send(output_packets.PushEntity(entity, request_id))

        event.wait()


def __on_disconnect():
    logger.info("Disconnected from Plames machine")
    mutable_data.plames_connection_inited = False


def __execute_func():

    while True:
        packet = mutable_data.executorQueue.get(True)
        __execute(packet)


def __execute(packet):

    input_stream = BytesIO()
    input_stream.write(packet._cached_input)
    input_stream.seek(0)

    packet.read(input_stream)

    input_stream.close()

    packet.on_received()

    if isinstance(packet, RequestEndpoint):
        send(packet)


def __write_packets():

    while True:
        '''
        while not mutable_data.plames_connection_inited:
            pass
        '''
        packet = mutable_data.packetsQueue.get(True)

        output = packet._cached_output.getvalue()

        mutable_data.clientSocket.send(struct.pack(">h", packet.get_id()))
        mutable_data.clientSocket.send(struct.pack(">i", len(output)))

        if isinstance(packet, JavaRequest) or isinstance(packet, RequestEndpoint):
            mutable_data.clientSocket.send(struct.pack(">q", packet.request_id))

        mutable_data.clientSocket.send(output)

        packet._cached_output.close()

        print("send packet: "+str(packet))

        del packet._cached_output


def __listen():

    try:

        while True:
            packet_id = struct.unpack(">h", mutable_data.clientSocket.recv(2, socket.MSG_WAITALL))[0]
            size = struct.unpack(">i", mutable_data.clientSocket.recv(4, socket.MSG_WAITALL))[0]

            packet = mutable_data.input_packet_registry.get(packet_id)()

            if isinstance(packet, JavaRequest) or isinstance(packet, RequestEndpoint):
                packet.request_id = struct.unpack(">q", mutable_data.clientSocket.recv(8, socket.MSG_WAITALL))[0]

            packet._cached_input = mutable_data.clientSocket.recv(size, socket.MSG_WAITALL)

            if isinstance(packet, JavaRequest):
                mutable_data.request_data_dict.update({packet.request_id: packet})
                mutable_data.request_events_dict.get(packet.request_id).set()
            else:
                mutable_data.executorQueue.put(packet)

    except ConnectionAbortedError:
        __on_disconnect()
