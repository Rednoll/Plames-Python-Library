from multiprocessing import Queue
from threading import Lock, Event


class MutableData(object):

    def __init__(self):
        self.agent_id = -1
        self.commands_registry = {}
        self.command_master_config = None
        self.classes_types = {}
        self.input_packet_registry = {}
        self.plames_connection_inited = False
        self.connect_lock = None
        self.clientSocket = None
        self.packetsQueue = Queue()
        self.request_events_dict = {}
        self.request_data_dict = {}
        self.next_request_id = 0
        self.request_id_lock = Lock()
        self.sender = None
        self.listener = None
        self.executor = None
        self.executorQueue = Queue()

mutable_data = MutableData()
