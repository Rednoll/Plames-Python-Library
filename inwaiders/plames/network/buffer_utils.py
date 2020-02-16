import socket
import struct
import array
import sys
from inwaiders.plames.network import class_type_utils, plames_client


class_types = class_type_utils


def write_utf8(output, _str):
    write_byte_array(output, _str.encode("utf-8"))


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
        write_data(output, sub)


def write_set(output, _object):
    size = len(_object)
    write_int(output, size)

    for sub in _object:
        write_data(sub)


def write_dict(output, _object):
    size = len(_object)
    write_int(output, size)

    for key in _object:
        write_data(key)
        write_data(_object[key])


def write_fields(output, _object, only_changes=False):

    _vars_type = _object.__types

    if only_changes:

        changed_vars = _object.__changed_vars

        write_int(output, len(changed_vars)) #add adaptive calc

        for var_name in changed_vars:

            var = _object.__dict__[var_name]

            write_utf8(output, var_name)
            write_data(output, var, _vars_type[var_name])

    else:

        vars_names = _object.__fields_names

        write_int(output, len(vars_names))

        for var_name in vars_names:

            var = _object.__dict__[var_name]

            write_utf8(output, var_name)
            write_data(output, var, _vars_type[var_name])


def write_data(output, _object, type_id=None):

    if type_id is None:
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

    elif type_id == class_types.OBJECT:
        write_utf8(_object.class_java_name)

        write_fields(output, _object)

    elif type_id == class_types.ENTITY:
        write_utf8(_object.class_java_name)
        write_long(_object.id)

        write_fields(output, _object, True)


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
        field_value.append(read_data(input_socket))

    return field_value


def read_set(input_socket):
    field_value = []

    size = read_int(input_socket)
    for i in range(0, size):
        field_value.append(read_data(input_socket))

    return field_value


def read_dict(input_socket):
    field_value = {}

    size = read_int(input_socket)
    for i in range(0, size):
        field_value.update({read_data(input_socket): read_data(input_socket)})

    return field_value


def read_data(input_socket, obj_type=None):

    if obj_type is None:
        obj_type = read_short(input_socket)

    if obj_type == class_types.NULL_TYPE:
        return None

    elif obj_type == class_types.BYTE_TYPE:
        return read_byte(input_socket)

    elif obj_type == class_types.CHAR_TYPE:
        return read_char(input_socket)

    elif obj_type == class_types.SHORT_TYPE:
        return read_short(input_socket)

    elif obj_type == class_types.INT_TYPE:
        return read_int(input_socket)

    elif obj_type == class_types.LONG_TYPE:
        return read_long(input_socket)

    elif obj_type == class_types.FLOAT_TYPE:
        return read_float(input_socket)

    elif obj_type == class_types.DOUBLE_TYPE:
        return read_double(input_socket)

    elif obj_type == class_types.STRING_TYPE:
        return read_utf8(input_socket)

    elif obj_type == class_types.BYTE_ARRAY_TYPE:
        return input_socket.recv(read_int(input_socket), socket.MSG_WAITALL)

    elif obj_type == class_types.CHAR_ARRAY_TYPE:
        return read_char_array(input_socket)

    elif obj_type == class_types.SHORT_ARRAY_TYPE:
        return read_short_array(input_socket)

    elif obj_type == class_types.INT_ARRAY_TYPE:
        return read_int_array(input_socket)

    elif obj_type == class_types.LONG_ARRAY_TYPE:
        return read_long_array(input_socket)

    elif obj_type == class_types.FLOAT_ARRAY_TYPE:
        return read_float_array(input_socket)

    elif obj_type == class_types.DOUBLE_ARRAY_TYPE:
        return read_double_array(input_socket)

    elif obj_type == class_types.STRING_ARRAY_TYPE:
        return read_string_array(input_socket)

    elif obj_type == class_types.LIST_TYPE:
        return read_list(input_socket)

    elif obj_type == class_types.SET_TYPE:
        return read_set(input_socket)

    elif obj_type == class_types.MAP_TYPE:
        return read_dict(input_socket)

    elif obj_type == class_types.BOOLEAN_TYPE:
        return read_boolean(input_socket)

    elif obj_type == class_types.BOOLEAN_ARRAY_TYPE:
        return read_boolean_array(input_socket)

    elif obj_type == class_types.OBJECT:
        class_java_name = read_utf8(input_socket)
        class_name = read_utf8(input_socket)
        super_class_java_name = read_utf8(input_socket)

        fields_data = read_fields(input_socket)

        new_object = type(class_name, (object,), fields_data[0])()

        new_object.class_java_name = class_java_name
        new_object.__types = fields_data[1]

        return new_object

    elif obj_type == class_types.ENTITY:
        class_java_name = read_utf8(input_socket)
        class_name = read_utf8(input_socket)
        super_class_java_name = read_utf8(input_socket)

        fields_data = read_fields(input_socket)

        def push(self):
            plames_client.push(self)

        fields_data[0].update({"push": push})

        new_object = type(class_name, (object,), fields_data[0])()

        new_object.class_java_name = class_java_name
        new_object.__types = fields_data[1]
        new_object.__fields_names = fields_data[2]
        new_object.__changed_vars = []
        new_object.is_entity = True

        return new_object

    return None


def read_fields(input_socket):

    fields_dict = {}
    fields_types_dict = {}
    fields_names = []

    fields_count = read_int(input_socket)

    for i in range(0, fields_count):
        field_name = to_snake_case(read_utf8(input_socket))
        field_type = read_short(input_socket)

        if class_type_utils.is_lazy(field_type):

            def get_f(self, field_name=field_name):

                if hasattr(self, "_"+field_name):
                    return getattr(self, "_"+field_name)
                else:
                    f_value = plames_client.request_attr(self.class_java_name, self.id, field_name)
                    setattr(self, "_"+field_name, f_value)
                    return f_value

            def set_f(self, value, field_name=field_name):

                setattr(self, "_"+field_name, value)

                if self.__changed_vars.count(field_name) == 0:
                    self.__changed_vars.append(field_name)

            field_value = property(get_f, set_f)

        else:
            field_value = read_data(input_socket, field_type)

        fields_dict.update({field_name: field_value})
        fields_types_dict.update({field_name: field_type})
        fields_names.append(field_name)
        # print(class_name + "." + field_name + ": " + str(field_value))
    return (fields_dict, fields_types_dict, fields_names)


def to_snake_case(_str):
    return ''.join(['_' + i.lower() if i.isupper() else i for i in _str]).lstrip('_')
