class Command(object):
    pass


class MessengerCommand(Command):

    def __init__(self):
        super().__init__()

        from inwaiders.plames.plames import mutable_data
        self.class_java_name = mutable_data.command_master_config["command_java_class"]

        self.aliases = []
        self.child_commands = []

    def run(self, profile, args=[]):
        raise RuntimeWarning("You need override run method!")