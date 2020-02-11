from inwaiders.plames.network import plames_client
from inwaiders.plames.network import data_packets

import struct

plames_client.connect("localhost", 9090)
plames_client.send(data_packets.RequestObject("User", ("Redn_oll", "test")))


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
