from inwaiders.plames.module.module_base import ModuleBase
import sys
import os
import importlib
from zipfile import ZipFile
from inwaiders.plames.network import plames_client
from inwaiders.plames.network import output_packets
import logging
from inwaiders.plames.command import command
import configparser
import time
from inwaiders.plames import mutable_data

logger = None
config_parser = configparser.ConfigParser()
client_config = None

modules = []


def main():
    global logger

    init_logger()
    load_configs()

    import_modules()
    load_modules()

    pre_init_modules()

    connect()

    init_modules()
    post_init_modules()

    plames_client.send(output_packets.BootLoaded())

def connect():
    global logger

    address = client_config["address"]
    port = int(client_config["port"])

    logger.info("Connecting to Plames machine "+address+":"+str(port))
    plames_client.connect(address, port)
    logger.info("Connecting complete. Hi, Plames!")


def load_configs():
    global client_config, logger

    config_parser.read("main.ini")

    client_config = config_parser["Plames JPC"]

    mutable_data.command_master_config = config_parser["Command Master"]

    logger.info("Configs loading complete!")


def init_logger():
    global logger

    logger = logging.getLogger("Plames")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("plames-logs.log")

    formatter = logging.Formatter('%(asctime)s %(levelname)6s %(thread)d --- [%(threadName)s] %(name)28s : %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("Logger init complete!")


def pre_init_modules():
    global logger

    logger.info("Begin pre initialization modules")

    for module in modules:
        module.pre_init()
        logger.info("Pre init \""+module.name+"\" complete!")

    logger.info("Pre initialization complete!")


def init_modules():
    global logger

    logger.info("Begin initialization modules")

    for module in modules:
        module.init()
        logger.info("Init \""+module.name+"\" complete!")

    logger.info("Initialization complete!")


def post_init_modules():
    global logger

    logger.info("Begin post initialization modules")

    for module in modules:
        module.post_init()
        logger.info("Post init \""+module.name+"\" complete!")

    logger.info("Post initialization complete!")


def import_modules():
    global logger

    logger.info("Importing modules...")

    for root, dirs, files in os.walk(".\modules"):

        for name in files:

            if not name.endswith(".zip"):
                continue

            file = os.path.join(root, name)
            sys.path.insert(0, file)

            with ZipFile(file, "r") as zipObj:

                module_files = zipObj.namelist()

                for module_file_name in module_files:

                    if "_module.py" in module_file_name:
                        importlib.import_module(module_file_name.replace(".py", ""))
                        logger.info("Import module: "+module_file_name)

    logger.info("Import complete!")


def load_modules():
    global modules

    classes_modules = ModuleBase.__subclasses__()

    logger.info("Loading modules...")

    for module_class in classes_modules:

        module = module_class()
        modules.append(module)
        logger.info("Load module: \""+module.name+"\" version: "+str(module.version))

    logger.info("Load complete!")


class Session(object):

    def __init__(self):
        self.object_map = {}
        
    def add_object(self, object, s_id=None):
        
        if s_id is None:
            self.object_map.update({s_id: object})
            object.__s_id = s_id
        else:
            self.object_map.update({object.__s_id: object})
    
    def get_object(self, s_id):
        return self.object_map.get(s_id)
    
    def has_object(self, object):
        
        if hasattr(object, "__s_id"):
            return self.get_object(object.__s_id) is non None
        else:
            for s_id in self.object_map:   
                if self.object_map.get(s_id) is object:
                    return True
    
if __name__ == "__main__":
    main()
