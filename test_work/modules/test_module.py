from inwaiders.plames.module.module_base import ModuleBase
from inwaiders.plames.command import command_registry, command
from inwaiders.plames.plames import plames_client

class TestModule(ModuleBase):

    def __init__(self):
        self.name = "Test Python Module"
        self.version = "1.0V"
        self.description = "Тестовый Python модуль!"
        self.type = "functional"
        self.license_key = None
        self.system_version = 0

    def pre_init(self):
        pass

    def init(self):
        command_registry.register_root(PythonMainCommand())

    def post_init(self):
        pass


class PythonMainCommand(command.MessengerCommand):

    def __init__(self):
        super().__init__()
        self.aliases.append("python")
        self.child_commands.append(PythonTestCommand())


class PythonTestCommand(command.MessengerCommand):

    def __init__(self):
        super().__init__()
        self.aliases.append("test")

    def run(self, profile, args=[]):
        MessageUtils = plames_client.request_static("com.inwaiders.plames.system.utils.MessageUtils")
        MessageUtils.send(profile, "Я питонова команда ахуеть и не встать!")

