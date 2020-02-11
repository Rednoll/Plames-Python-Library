import array

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

def getClassType(obj):

    if type(obj) == bool:
        return BOOLEAN_TYPE
    if type(obj) == int:
        return LONG_TYPE
    if type(obj) == chr:
        return CHAR_TYPE
    if type(obj) == float:
        return DOUBLE_TYPE
    if type(obj) == str:
        return STRING_TYPE
    if type(obj) == array.array:
        if obj.typecode == 'b':
            return BYTE_ARRAY_TYPE
        if obj.typecode == 'h':
            return SHORT_ARRAY_TYPE
        if obj.typecode == 'u':
            return CHAR_ARRAY_TYPE
        if obj.typecode == 'l':
            return INT_ARRAY_TYPE
        if obj.typecode == 'q':
            return LONG_ARRAY_TYPE
        if obj.typecode == 'f':
            return FLOAT_ARRAY_TYPE
        if obj.typecode == 'd':
            return DOUBLE_ARRAY_TYPE
    if type(obj) == list:
        return LIST_TYPE
    if type(obj) == tuple:
        return LIST_TYPE
    if type(obj) == dict:
        return MAP_TYPE
