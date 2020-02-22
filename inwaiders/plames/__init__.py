class MutableData(object):

    def __init__(self):
        self.agent_id = -1
        self.commands_registry = {}
        self.command_master_config = None

mutable_data = MutableData()