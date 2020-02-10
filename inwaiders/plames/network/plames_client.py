import socket
import struct
import threading
from multiprocessing import Queue

from inwaiders.plames.network import java_answer

clientSocket = None
packetsQueue = Queue()
sender = None
listener = None


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