import array
from inwaiders.plames import plames

ENTITY_LINK = -5
STATIC = -4
LINK = -3
ENTITY = -2
OBJECT = -1

BYTE_TYPE = 0
CHAR_TYPE = 1
SHORT_TYPE = 2
INT_TYPE = 3
LONG_TYPE = 4
FLOAT_TYPE = 5
DOUBLE_TYPE = 6
STRING_TYPE = 7
LIST_TYPE = 8
SET_TYPE = 9
MAP_TYPE = 10
BYTE_ARRAY_TYPE = 11
CHAR_ARRAY_TYPE = 12
SHORT_ARRAY_TYPE = 13
INT_ARRAY_TYPE = 14
LONG_ARRAY_TYPE = 15
FLOAT_ARRAY_TYPE = 16
DOUBLE_ARRAY_TYPE = 17
STRING_ARRAY_TYPE = 18
NULL_TYPE = 19
BOOLEAN_TYPE = 20
BOOLEAN_ARRAY_TYPE = 21
LOCALE = 22
LAZY_LIST = 23
LAZY_SET = 24
LAZY_MAP = 25


def get_class_fields_types(class_java_name):

    from inwaiders.plames.network import plames_client, request_packets

    cached = plames.mutable_data.classes_types.get(class_java_name)

    if cached is not None:
        return cached
    else:
        types = plames_client.request(request_packets.ClassTypesRequest(class_java_name)).types
        plames.mutable_data.classes_types.update({class_java_name: types})
        return types


def get_class_type(obj):

    if type(obj) == bool:
        return BOOLEAN_TYPE
    elif type(obj) == int:
        return LONG_TYPE
    elif type(obj) == chr:
        return CHAR_TYPE
    elif type(obj) == float:
        return DOUBLE_TYPE
    elif type(obj) == str:
        return STRING_TYPE
    elif type(obj) == array.array:
        if obj.typecode == 'b':
            return BYTE_ARRAY_TYPE
        elif obj.typecode == 'h':
            return SHORT_ARRAY_TYPE
        elif obj.typecode == 'u':
            return CHAR_ARRAY_TYPE
        elif obj.typecode == 'l':
            return INT_ARRAY_TYPE
        elif obj.typecode == 'q':
            return LONG_ARRAY_TYPE
        elif obj.typecode == 'f':
            return FLOAT_ARRAY_TYPE
        elif obj.typecode == 'd':
            return DOUBLE_ARRAY_TYPE
    elif type(obj) == list:
        return LIST_TYPE
    elif type(obj) == tuple:
        return LIST_TYPE
    elif type(obj) == dict:
        return MAP_TYPE
    elif hasattr(obj, "is_entity") and obj.is_entity:
        return ENTITY
    elif hasattr(obj, "is_static") and obj.is_static:
        return STATIC
    elif hasattr(obj, "is_entity_link") and obj.is_entity_link:
        return ENTITY_LINK

    return OBJECT


def is_lazy(type):
    if type == LAZY_LIST:
        return True
    if type == LAZY_SET:
        return True
    if type == LAZY_MAP:
        return True
    return False


def is_cacheable(type):
    if type == OBJECT:
        return True
    if type == ENTITY:
        return True
    return False
