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
        MessageUtils.send(profile, "Я питонова команда!")

        '''
        CurrencyAccountImpl = plames_client.request_static("com.inwaiders.plames.modules.wallet.domain.account.impl.CurrencyAccountImpl")
        CurrencyImpl = plames_client.request_static("com.inwaiders.plames.modules.wallet.domain.currency.impl.CurrencyImpl")

        currency = CurrencyImpl.parse_by_sign("dnt")

        user = profile.get_user()

        bill = plames_client.create("CurrencyBill", (user, 10))
        bill.description = "Test python bill creation!"
        bill.account = CurrencyAccountImpl.parse_account(currency, "private", user, True)
        bill.currency_amount = 1000
        bill.profile = profile
        '''