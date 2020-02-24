class MutableData(object):

    def __init__(self):
        self.agent_id = -1
        self.commands_registry = {}
        self.command_master_config = None
        self.classes_types = {}
        self.input_packet_registry = {}

mutable_data = MutableData()