class Command(object):

    _id = -1


class MessengerCommand(Command):

    aliases = []
    child_commands = []

    def run(self, profile, args=[]):
        raise RuntimeWarning("You need override run method!")