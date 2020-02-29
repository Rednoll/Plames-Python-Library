import logging
from inwaiders.plames import mutable_data
from inwaiders.plames.network import class_type_utils

next_command_id = 0

logger = logging.getLogger("Plames.Command-Registry")


def register_root(root_command):

    if root_command in mutable_data.commands_roots_registry.values():
        return False

    register_command(root_command)

    mutable_data.commands_roots_registry.update({root_command.python_id: root_command})
    logger.info("Registered root \""+root_command.aliases[0]+"\"")


def register_command(command):

    if command in mutable_data.commands_registry.values():
        return False

    command_id = get_new_command_id()
    command.python_id = command_id

    mutable_data.commands_registry.update({command_id: command})
    logger.info("Registered command \""+command.aliases[0]+"\" id: "+str(command_id))

    for sub_command in command.child_commands:
        register_command(sub_command)

    return True


def get_command(command_id):
    return mutable_data.commands_registry.get(command_id)


def get_new_command_id():
    global next_command_id

    current = next_command_id
    next_command_id += 1
    return current
