import logging
from inwaiders.plames import mutable_data
from inwaiders.plames.network import class_type_utils

next_command_id = 0

logger = logging.getLogger("Plames.Command-Registry")


def register_command(command):
    command_id = get_new_command_id()
    command.python_id = command_id
    mutable_data.commands_registry.update({command_id: command})
    logger.info("Registered command \""+command.aliases[0]+"\" id: "+str(command_id))


def get_new_command_id():
    global next_command_id

    current = next_command_id
    next_command_id += 1
    return current
