class ModuleBase(object):

    name = None
    version = None
    description = None
    type = None
    license_key = None
    system_version = 0

    def pre_init(self):
        pass

    def init(self):
        pass

    def post_init(self):
        pass
