import socket
import struct
import array
import sys
from inwaiders.plames.network import class_type_utils

class_types = class_type_utils

def write_utf8(output, str):
    write_byte_array(output, str.encode("utf-8"))

def write_byte_array(output, byte_array):
    output.extend(struct.pack(">i", len(byte_array)))
    output.extend(byte_array)

def write_byte(output, _byte):
    output.extend(struct.pack(">b", _byte))

def write_int(output, _int):
    output.extend(struct.pack(">i", _int))

def write_short(output, _short):
    output.extend(struct.pack(">h", _short))

def write_char(output, _char):
    output.extend(struct.pack(">h", _char))

def write_long(output, _long):
    output.extend(struct.pack(">q", _long))

def write_float(output, _float):
    output.extend(struct.pack(">f", _float))

def write_double(output, _double):
    output.extend(struct.pack(">d", _double))

def write_boolean(output, _boolean):
    write_byte(output, 1 if _boolean else 0)

def write_boolean_array(output, _object):
    size = len(_object)
    write_int(size)

    for sub in _object:
        write_boolean(output, sub)

def write_short_array(output, _object):
    size = len(_object)
    write_int(size)

    for sub in _object:
        write_short(output, sub)

def write_char_array(output, _object):
    size = len(_object)
    write_int(size)

    for sub in _object:
        write_char(output, sub)

def write_int_array(output, _object):
    size = len(_object)
    write_int(size)

    for sub in _object:
        write_int(output, sub)

def write_long_array(output, _object):
    size = len(_object)
    write_int(size)

    for sub in _object:
        write_long(output, sub)

def write_float_array(output, _object):
    size = len(_object)
    write_int(size)

    for sub in _object:
        write_float(output, sub)

def write_double_array(output, _object):
    size = len(_object)
    write_int(size)

    for sub in _object:
        write_double(output, sub)

def write_string_array(output, _object):
    size = len(_object)
    write_int(size)

    for sub in _object:
        write_utf8(output, sub)

def write_list(output, _object):
    size = len(_object)
    write_int(output, size)

    for sub in _object:
        write_object(output, sub)

def write_set(output, _object):
    size = len(_object)
    write_int(output, size)

    for sub in _object:
        write_object(sub)

def write_dict(output, _object):
    size = len(_object)
    write_int(output, size)

    for key in _object:
        write_object(key)
        write_object(_object[key])

def write_object(output, _object):

    type_id = class_types.getClassType(_object)

    write_short(output, type_id)

    if type_id == class_types.BOOLEAN_TYPE:
        write_boolean(output, _object)

    elif type_id == class_types.BYTE_TYPE:
        write_byte(output, _object)

    elif type_id == class_types.SHORT_TYPE:
        write_short(output, _object)

    elif type_id == class_types.CHAR_TYPE:
        write_char(output, _object)

    elif type_id == class_types.INT_TYPE:
        write_int(output, _object)

    elif type_id == class_types.LONG_TYPE:
        write_long(output, _object)

    elif type_id == class_types.FLOAT_TYPE:
        write_float(output, _object)

    elif type_id == class_types.DOUBLE_TYPE:
        write_double(output, _object)

    elif type_id == class_types.STRING_TYPE:
        write_utf8(output, _object)

    elif type_id == class_types.NULL_TYPE:
        pass

    elif type_id == class_types.BOOLEAN_ARRAY_TYPE:
        write_boolean_array(output, _object)

    elif type_id == class_types.BYTE_ARRAY_TYPE:
        write_byte_array(output, _object)

    elif type_id == class_types.SHORT_ARRAY_TYPE:
        write_short_array(output, _object)

    elif type_id == class_types.CHAR_ARRAY_TYPE:
        write_char_array(output, _object)

    elif type_id == class_types.INT_ARRAY_TYPE:
        write_int_array(output, _object)

    elif type_id == class_types.LONG_ARRAY_TYPE:
        write_long_array(output, _object)

    elif type_id == class_types.FLOAT_ARRAY_TYPE:
        write_float_array(output, _object)

    elif type_id == class_types.DOUBLE_ARRAY_TYPE:
        write_double_array(output, _object)

    elif type_id == class_types.STRING_ARRAY_TYPE:
        write_string_array(output, _object)

    elif type_id == class_types.LIST_TYPE:
        write_list(output, _object)

    elif type_id == class_types.SET_TYPE:
        write_set(output, _object)

    elif type_id == class_types.MAP_TYPE:
        write_dict(output, _object)

    else:
        write_utf8(_object.class_java_name)

        _vars = _object.__dict__
        write_int(output, len(_vars))

        for var_name in _vars:

            var = _vars[var_name]

            if callable(var):
                continue

            write_utf8(output, var_name)
            write_object(output, var)


def read_boolean(input_socket):
    return read_byte(input_socket) == 1

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
    return chr(struct.unpack(">h", input_socket.recv(2, socket.MSG_WAITALL))[0])

def read_long(input_socket):
    return struct.unpack(">q", input_socket.recv(8, socket.MSG_WAITALL))[0]

def read_float(input_socket):
    return struct.unpack(">f", input_socket.recv(4, socket.MSG_WAITALL))[0]

def read_double(input_socket):
    return struct.unpack(">d", input_socket.recv(8, socket.MSG_WAITALL))[0]

def read_char_array(input_socket):
    field_value = array.array("u")

    size = read_int(input_socket)
    for i in range(0, size):
        field_value.append(read_char(input_socket))

    return field_value

def read_short_array(input_socket):
    field_value = array.array("h")

    size = read_int(input_socket)
    for i in range(0, size):
        field_value.append(read_short(input_socket))

    return field_value

def read_int_array(input_socket):
    field_value = array.array("l")

    size = read_int(input_socket)
    for i in range(0, size):
        field_value.append(read_int(input_socket))

    return field_value

def read_long_array(input_socket):
    field_value = array.array("q")

    size = read_int(input_socket)
    for i in range(0, size):
        field_value.append(read_long(input_socket))

    return field_value

def read_float_array(input_socket):
    field_value = array.array("f")

    size = read_int(input_socket)
    for i in range(0, size):
        field_value.append(read_float(input_socket))

    return field_value

def read_double_array(input_socket):
    field_value = array.array("d")

    size = read_int(input_socket)
    for i in range(0, size):
        field_value.append(read_double(input_socket))

    return field_value

def read_string_array(input_socket):
    field_value = []

    size = read_int(input_socket)
    for i in range(0, size):
        field_value.append(read_utf8(input_socket))

    return field_value

def read_boolean_array(input_socket):
    field_value = []

    size = read_int(input_socket)
    for i in range(0, size):
        field_value.append(read_boolean(input_socket))

    return field_value

def read_list(input_socket):
    field_value = []

    size = read_int(input_socket)
    for i in range(0, size):
        field_value.append(read_object(input_socket))

    return field_value

def read_set(input_socket):
    field_value = []

    size = read_int(input_socket)
    for i in range(0, size):
        field_value.append(read_object(input_socket))

    return field_value

def read_dict(input_socket):
    field_value = {}

    size = read_int(input_socket)
    for i in range(0, size):
        field_value.update({read_object(input_socket): read_object(input_socket)})

    return field_value

def read_object(input_socket):

    field_type = read_short(input_socket)

    if field_type == class_types.NULL_TYPE:
        return None

    if field_type == class_types.BYTE_TYPE:
        return read_byte(input_socket)

    if field_type == class_types.CHAR_TYPE:
        return read_char(input_socket)

    if field_type == class_types.SHORT_TYPE:
        return read_short(input_socket)

    if field_type == class_types.INT_TYPE:
        return read_int(input_socket)

    if field_type == class_types.LONG_TYPE:
        return read_long(input_socket)

    if field_type == class_types.FLOAT_TYPE:
        return read_float(input_socket)

    if field_type == class_types.DOUBLE_TYPE:
        return read_double(input_socket)

    if field_type == class_types.STRING_TYPE:
        return read_utf8(input_socket)

    if field_type == class_types.BYTE_ARRAY_TYPE:
        return input_socket.recv(read_int(input_socket), socket.MSG_WAITALL)

    if field_type == class_types.CHAR_ARRAY_TYPE:
        return read_char_array(input_socket)

    if field_type == class_types.SHORT_ARRAY_TYPE:
        return read_short_array(input_socket)

    if field_type == class_types.INT_ARRAY_TYPE:
        return read_int_array(input_socket)

    if field_type == class_types.LONG_ARRAY_TYPE:
        return read_long_array(input_socket)

    if field_type == class_types.FLOAT_ARRAY_TYPE:
        return read_float_array(input_socket)

    if field_type == class_types.DOUBLE_ARRAY_TYPE:
        return read_double_array(input_socket)

    if field_type == class_types.STRING_ARRAY_TYPE:
        return read_string_array(input_socket)

    if field_type == class_types.LIST_TYPE:
        return read_list(input_socket)

    if field_type == class_types.SET_TYPE:
        return read_set(input_socket)

    if field_type == class_types.MAP_TYPE:
        return read_dict(input_socket)

    if field_type == class_types.BOOLEAN_TYPE:
        return read_boolean(input_socket)

    if field_type == class_types.BOOLEAN_ARRAY_TYPE:
        return read_boolean_array(input_socket)

    else:
        class_java_name = read_utf8(input_socket)
        class_name = read_utf8(input_socket)
        super_class_java_name = read_utf8(input_socket)
        fields_count = read_int(input_socket)

        fields_dict = {}

        for i in range(0, fields_count):
            field_name = to_snake_case(read_utf8(input_socket))
            field_value = read_object(input_socket)

            print(field_name+": "+str(field_value))

            fields_dict.update({field_name: field_value})

        new_object = type(class_name, (), fields_dict)

        new_object.class_java_name = class_java_name

        return new_object


def to_snake_case(_str):
    return ''.join(['_' + i.lower() if i.isupper() else i for i in _str]).lstrip('_')
