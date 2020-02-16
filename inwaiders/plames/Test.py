from inwaiders.plames.network import plames_client
from inwaiders.plames.network import data_packets

import time
import struct
import cProfile

plames_client.connect("localhost", 9090)

def test():

    test_entity = plames_client.request("TestEntity", "getById", [44804])

    print(test_entity.test_long)

    test_entity.test_long = -7

    print(test_entity.test_long)

    test_entity.push()

test()

'''
sock = socket.socket()
sock.connect(("localhost", 9090))

packet_id = struct.unpack(">h", sock.recv(2, socket.MSG_WAITALL))[0]
data_length = struct.unpack(">i", sock.recv(4, socket.MSG_WAITALL))[0]
data = sock.recv(data_length, socket.MSG_WAITALL)

print("data_length: "+str(data_length))
print("packet_id: "+str(packet_id))
print("data: "+data.decode("utf-8"))

toSend = "Hello java!"
'''
