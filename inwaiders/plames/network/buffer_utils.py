import socket
import struct
import array


def read_utf8(input_socket):
    size = read_int(input_socket)
    return input_socket.recv(size, socket.MSG_WAITALL).decode("utf-8")

def read_byte(input_socket):
    return struct.unpack(">b", input_socket.recv(1, socket.MSG_WAITALL))[0]

def read_int(input_socket):
    return struct.unpack(">i", input_socket.recv(4, socket.MSG_WAITALL))[0]

def read_short(input_socket):
    return struct.unpack(">h", input_socket.recv(2, socket.MSG_WAITALL))[0]

def read_char(input_socket):
    return struct.unpack(">h", input_socket.recv(2, socket.MSG_WAITALL))[0]

def read_long(input_socket):
    return struct.unpack(">Q", input_socket.recv(8, socket.MSG_WAITALL))[0]

def read_float(input_socket):
    return struct.unpack(">f", input_socket.recv(4, socket.MSG_WAITALL))[0]

def read_double(input_socket):
    return struct.unpack(">d", input_socket.recv(8, socket.MSG_WAITALL))[0]

def read_object(input_socket):
    clazz_name = read_utf8(input_socket)
    super_clazz = read_utf8(input_socket)
    fields_count = read_int(input_socket)

    fields_dict = {}

    for i in range(0, fields_count):
        field_name = read_utf8(input_socket)
        field_value = __read_attribute(input_socket)

        fields_dict.update({field_name: field_value})

    return type(clazz_name, globals()[super_clazz](), fields_dict)

def __read_attribute(input_socket):

    field_type = read_short(input_socket)

    if field_type == 0:
        return read_byte(input_socket)
    if field_type == 1:
        return read_char(input_socket)
    if field_type == 2:
        return read_char(input_socket)
    if field_type == 3:
        return read_int(input_socket)
    if field_type == 4:
        return read_long(input_socket)
    if field_type == 5:
        return read_float(input_socket)
    if field_type == 6:
        return read_double(input_socket)
    if field_type == 7:
        return read_utf8(input_socket)
    if field_type == 11:
        return input_socket.recv(read_int(input_socket), socket.MSG_WAITALL)
    if field_type == 12:
        field_value = array.array("h")
        field_value.frombytes(input_socket.recv(read_int(input_socket) * 2, socket.MSG_WAITALL))
        return field_value
    if field_type == 13:
        field_value = array.array("h")
        field_value.frombytes(input_socket.recv(read_int(input_socket) * 2, socket.MSG_WAITALL))
        return field_value
    if field_type == 14:
        field_value = array.array("l")
        field_value.frombytes(input_socket.recv(read_int(input_socket) * 4, socket.MSG_WAITALL))
        return field_value
    if field_type == 15:
        field_value = array.array("q")
        field_value.frombytes(input_socket.recv(read_int(input_socket) * 8, socket.MSG_WAITALL))
        return field_value
    if field_type == 16:
        field_value = array.array("f")
        field_value.frombytes(input_socket.recv(read_int(input_socket) * 4, socket.MSG_WAITALL))
        return field_value
    if field_type == 17:
        field_value = array.array("d")
        field_value.frombytes(input_socket.recv(read_int(input_socket) * 8, socket.MSG_WAITALL))
        return field_value
    if field_type == 18:
        field_value = []
        strings_count = read_int(input_socket)
        for j in range(0, strings_count):
            field_value.append(read_utf8(input_socket))
        return field_value