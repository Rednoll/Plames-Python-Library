import socket
import struct
import array
import sys
from builtins import hasattr

from inwaiders.plames.network import class_type_utils, plames_client

class_types = class_type_utils

transient_fields = ["__types", "__fields_names", "class_java_name", "_s_id", "__root", "_dirty"]


def write_utf8(output, _str):
    write_byte_array(output, _str.encode("utf-8"))


def write_byte_array(output, byte_array):
    write_int(output, len(byte_array))
    output.write(byte_array)


def write_byte(output, _byte):
    output.write(struct.pack(">b", _byte))


def write_int(output, _int):
    output.write(struct.pack(">i", _int))


def write_short(output, _short):
    output.write(struct.pack(">h", _short))


def write_char(output, _char):
    output.write(struct.pack(">h", _char))


def write_long(output, _long):
    output.write(struct.pack(">q", _long))


def write_float(output, _float):
    output.write(struct.pack(">f", _float))


def write_double(output, _double):
    output.write(struct.pack(">d", _double))


def write_boolean(output, _boolean):
    write_byte(output, 1 if _boolean else 0)


def write_boolean_array(output, _object):
    size = len(_object)
    write_int(output, size)

    for sub in _object:
        write_boolean(output, sub)


def write_short_array(output, _object):
    size = len(_object)
    write_int(output, size)

    for sub in _object:
        write_short(output, sub)


def write_char_array(output, _object):
    size = len(_object)
    write_int(output, size)

    for sub in _object:
        write_char(output, sub)


def write_int_array(output, _object):
    size = len(_object)
    write_int(output, size)

    for sub in _object:
        write_int(output, sub)


def write_long_array(output, _object):
    size = len(_object)
    write_int(output, size)

    for sub in _object:
        write_long(output, sub)


def write_float_array(output, _object):
    size = len(_object)
    write_int(output, size)

    for sub in _object:
        write_float(output, sub)


def write_double_array(output, _object):
    size = len(_object)
    write_int(output, size)

    for sub in _object:
        write_double(output, sub)


def write_string_array(output, _object):
    size = len(_object)
    write_int(output, size)

    for sub in _object:
        write_utf8(output, sub)


def write_list(output, _object, session=None):
    size = len(_object)
    write_int(output, size)

    for sub in _object:
        write_data(output, sub, session)


def write_set(output, _object, session=None):
    size = len(_object)
    write_int(output, size)

    for sub in _object:
        write_data(output, sub, session)


def write_dict(output, _object, session=None):
    size = len(_object)
    write_int(output, size)

    for key in _object:
        write_data(output, key, session)
        write_data(output, _object[key], session)


def write_fields(output, _object, only_changes=False, session=None):

    if not hasattr(_object, "__types"):
        _object.__types = class_type_utils.get_class_fields_types(_object.class_java_name)

    vars_types = _object.__types

    if only_changes and hasattr(_object, "__changed_vars"):

        changed_vars = _object.__changed_vars

        write_int(output, len(changed_vars))

        for var_name in changed_vars:

            var = getattr(_object, "_"+var_name)

            write_utf8(output, to_camel_case(var_name))
            write_data(output, var, session, vars_types[to_camel_case(var_name)])

    else:

        if hasattr(_object, "__changed_vars"):
            vars_names = _object.__changed_vars
        else:
            vars_names = list(_object.__dict__.keys())

        for var_name in vars_names:
            if var_name in transient_fields:
                vars_names.remove(var_name)

        write_int(output, len(vars_names))

        for var_name in vars_names:

            if hasattr(_object, "__changed_vars"):
                var = getattr(_object, "_"+var_name)
            else:
                var = getattr(_object, var_name)

            write_utf8(output, to_camel_case(var_name))
            write_data(output, var, session, vars_types[to_camel_case(var_name)])


def write_entity(output, entity, session=None):
    write_utf8(output, entity.class_java_name)
    write_long(output, entity.id)
    write_int(output, entity._s_id)

    write_fields(output, entity, True, session)

    entity._dirty = False


def write_object(output, _object, session=None):
    write_utf8(output, _object.class_java_name)

    if hasattr(_object, "_s_id"):
        write_int(output, _object._s_id)
    else:
        write_int(output, -1)

    write_fields(output, _object, True, session)

    _object._dirty = False


def write_data(output, _object, session=None, type_id=None):

    if type_id is None:
       type_id = class_types.get_class_type(_object)

    if class_types.is_cacheable(type_id):

        if session.is_mapped(_object):
            write_short(output, class_types.LINK)
            write_int(output, session.get_cache_id(_object))
            return

    write_short(output, type_id);

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
        write_list(output, _object, session)

    elif type_id == class_types.SET_TYPE:
        write_set(output, _object, session)

    elif type_id == class_types.MAP_TYPE:
        write_dict(output, _object, session)

    elif type_id == class_types.OBJECT:
        write_object(output, _object, session)

    elif type_id == class_types.ENTITY:
        write_entity(output, _object, session)


def read_boolean(input_stream):
    return read_byte(input_stream) == 1


def read_utf8(input_stream):
    size = read_int(input_stream)
    return input_stream.read(size).decode("utf-8")


def read_byte(input_stream):
    return struct.unpack(">b", input_stream.read(1))[0]


def read_int(input_stream):
    return struct.unpack(">i", input_stream.read(4))[0]


def read_short(input_stream):
    return struct.unpack(">h", input_stream.read(2))[0]


def read_char(input_stream):
    return chr(struct.unpack(">h", input_stream.read(2))[0])


def read_long(input_stream):
    return struct.unpack(">q", input_stream.read(8))[0]


def read_float(input_stream):
    return struct.unpack(">f", input_stream.read(4))[0]


def read_double(input_stream):
    return struct.unpack(">d", input_stream.read(8))[0]


def read_char_array(input_stream):
    field_value = array.array("u")

    size = read_int(input_stream)
    for i in range(0, size):
        field_value.append(read_char(input_stream))

    return field_value


def read_short_array(input_stream):
    field_value = array.array("h")

    size = read_int(input_stream)
    for i in range(0, size):
        field_value.append(read_short(input_stream))

    return field_value


def read_int_array(input_stream):
    field_value = array.array("l")

    size = read_int(input_stream)
    for i in range(0, size):
        field_value.append(read_int(input_stream))

    return field_value


def read_long_array(input_stream):
    field_value = array.array("q")

    size = read_int(input_stream)
    for i in range(0, size):
        field_value.append(read_long(input_stream))

    return field_value


def read_float_array(input_stream):
    field_value = array.array("f")

    size = read_int(input_stream)
    for i in range(0, size):
        field_value.append(read_float(input_stream))

    return field_value


def read_double_array(input_stream):
    field_value = array.array("d")

    size = read_int(input_stream)
    for i in range(0, size):
        field_value.append(read_double(input_stream))

    return field_value


def read_string_array(input_stream):
    field_value = []

    size = read_int(input_stream)
    for i in range(0, size):
        field_value.append(read_utf8(input_stream))

    return field_value


def read_boolean_array(input_stream):
    field_value = []

    size = read_int(input_stream)
    for i in range(0, size):
        field_value.append(read_boolean(input_stream))

    return field_value


def read_list(input_stream, session):
    field_value = []

    size = read_int(input_stream)
    for i in range(0, size):
        field_value.append(read_data(input_stream, session))

    return field_value


def read_set(input_stream, session):
    field_value = []

    size = read_int(input_stream)

    for i in range(0, size):
        field_value.append(read_data(input_stream, session))

    return field_value


def read_dict(input_stream, session):
    field_value = {}

    size = read_int(input_stream)

    for i in range(0, size):
        field_value.update({read_data(input_stream, session): read_data(input_stream, session)})

    return field_value


def read_method(input, subject):

    method_name = read_utf8(input)

    def method(subject=subject, method_name=method_name, *args):
        return plames_client.request_run_method(subject._s_id, method_name, args)

    setattr(subject, to_snake_case(method_name), method)


def read_methods(input, subject):

    count = read_int(input)

    for i in range(0, count):

        read_method(input, subject)


def read_entity(input_stream, session):

    class_java_name = read_utf8(input_stream)
    class_name = read_utf8(input_stream)
    super_class_java_name = read_utf8(input_stream)
    s_id = read_int(input_stream)
   
    fields_data = read_fields(input_stream, session)

    def push(self, block=False):
        plames_client.push(self, block)

    fields_data[0].update({"push": push})

    def mark_as_dirty(self):
        self._dirty = True

    fields_data[0].update({"mark_as_dirty": mark_as_dirty})

    new_object = type(class_name, (object,), fields_data[0])()

    read_methods(input_stream, new_object)

    new_object.class_java_name = class_java_name
    new_object.__types = fields_data[1]
    new_object.__fields_names = fields_data[2]
    new_object.__changed_vars = []
    new_object.is_entity = True
    new_object._s_id = s_id
    
    session.add_object(new_object, s_id)
    
    return new_object


def read_object(input_stream, session):

    class_java_name = read_utf8(input_stream)
    class_name = read_utf8(input_stream)
    super_class_java_name = read_utf8(input_stream)
    s_id = read_int(input_stream)

    fields_data = read_fields(input_stream, session)

    def mark_as_dirty(self):
        self._dirty = True
        print("keke")

    fields_data[0].update({"mark_as_dirty": mark_as_dirty})

    new_object = type(class_name, (object,), fields_data[0])()

    read_methods(input_stream, new_object)

    new_object.class_java_name = class_java_name
    new_object.__types = fields_data[1]
    new_object.__fields_names = fields_data[2]
    new_object.__changed_vars = []
    new_object._s_id = s_id
    
    session.add_object(new_object, s_id)
    
    return new_object


def read_data(input_stream, session, obj_type=None):

    if obj_type is None:
        obj_type = read_short(input_stream)

    if obj_type == class_types.NULL_TYPE:
        return None

    elif obj_type == class_types.BYTE_TYPE:
        return read_byte(input_stream)

    elif obj_type == class_types.CHAR_TYPE:
        return read_char(input_stream)

    elif obj_type == class_types.SHORT_TYPE:
        return read_short(input_stream)

    elif obj_type == class_types.INT_TYPE:
        return read_int(input_stream)

    elif obj_type == class_types.LONG_TYPE:
        return read_long(input_stream)

    elif obj_type == class_types.FLOAT_TYPE:
        return read_float(input_stream)

    elif obj_type == class_types.DOUBLE_TYPE:
        return read_double(input_stream)

    elif obj_type == class_types.STRING_TYPE:
        return read_utf8(input_stream)

    elif obj_type == class_types.BYTE_ARRAY_TYPE:
        return input_stream.read(read_int(input_stream))

    elif obj_type == class_types.CHAR_ARRAY_TYPE:
        return read_char_array(input_stream)

    elif obj_type == class_types.SHORT_ARRAY_TYPE:
        return read_short_array(input_stream)

    elif obj_type == class_types.INT_ARRAY_TYPE:
        return read_int_array(input_stream)

    elif obj_type == class_types.LONG_ARRAY_TYPE:
        return read_long_array(input_stream)

    elif obj_type == class_types.FLOAT_ARRAY_TYPE:
        return read_float_array(input_stream)

    elif obj_type == class_types.DOUBLE_ARRAY_TYPE:
        return read_double_array(input_stream)

    elif obj_type == class_types.STRING_ARRAY_TYPE:
        return read_string_array(input_stream)

    elif obj_type == class_types.LIST_TYPE:
        return read_list(input_stream, session)

    elif obj_type == class_types.SET_TYPE:
        return read_set(input_stream, session)

    elif obj_type == class_types.MAP_TYPE:
        return read_dict(input_stream, session)

    elif obj_type == class_types.BOOLEAN_TYPE:
        return read_boolean(input_stream)

    elif obj_type == class_types.BOOLEAN_ARRAY_TYPE:
        return read_boolean_array(input_stream)

    elif obj_type == class_types.LINK:
        assert False, "Link can be read only like field!"

    elif obj_type == class_types.OBJECT:
        return read_object(input_stream, session)

    elif obj_type == class_types.ENTITY:
        return read_entity(input_stream, session)

    return None


def read_fields(input_stream, session):

    fields_dict = {}
    fields_types_dict = {}
    fields_names = []

    fields_count = read_int(input_stream)

    for i in range(0, fields_count):
        java_field_name = read_utf8(input_stream)
        field_name = to_snake_case(java_field_name)
        field_type = read_short(input_stream)

        def set_f(self, value, field_name=field_name):

            setattr(self, "_" + field_name, value)

            if field_name not in self.__changed_vars:
                self.__changed_vars.append(field_name)
                self.mark_as_dirty()

        if class_type_utils.is_lazy(field_type):

            def get_f(self, field_name=field_name):

                if hasattr(self, "_"+field_name):
                    return getattr(self, "_"+field_name)
                else:
                    value = plames_client.request_attr(self._s_id, to_camel_case(field_name))
                    setattr(self, "_"+field_name, value)
                    return value

            field_value = property(get_f, set_f)

        elif field_type == class_types.LINK:

            s_id = read_int(input_stream)

            def get_f(self, field_name=field_name, session=session, s_id=s_id):

                if hasattr(self, "_"+field_name):
                    return getattr(self, "_"+field_name)
                else:
                    value = session.get_object(s_id)
                    setattr(self, "_"+field_name, value)
                    return value

            field_value = property(get_f, set_f)

        else:

            def get_f(self, field_name=field_name):

                if hasattr(self, "_"+field_name):
                    value = getattr(self, "_"+field_name)
                    return value
                else:
                    return None

            fields_dict.update({"_"+field_name: read_data(input_stream, session, field_type)})
            field_value = property(get_f, set_f)

        fields_dict.update({field_name: field_value})
        fields_types_dict.update({to_camel_case(field_name): field_type})
        fields_names.append(field_name)
        #print(field_name + ": " + str(field_value))

    return fields_dict, fields_types_dict, fields_names


def to_snake_case(_str):
    return ''.join(['_' + i.lower() if i.isupper() else i for i in _str]).lstrip('_')


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])
