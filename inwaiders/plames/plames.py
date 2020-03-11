from pip._internal import req

from inwaiders.plames.module.module_base import ModuleBase
import sys
import os
import importlib
from zipfile import ZipFile
from inwaiders.plames.network import plames_client
from inwaiders.plames.network import output_packets
from inwaiders.plames.network import request_packets
import logging
from inwaiders.plames.command import command
import configparser
import time
from inwaiders.plames import mutable_data
import threading

logger = None
config_parser = configparser.ConfigParser()
client_config = None

modules = []

hyper_task_executor = None


def main():
    global logger, hyper_task_executor

    init_logger()
    load_configs()

    import_modules()
    load_modules()

    pre_init_modules()

    connect()

    init_modules()
    post_init_modules()

    hyper_task_executor = threading.Thread(target=__run_hyper_task_cycle)
    hyper_task_executor.start()

    plames_client.send(output_packets.BootLoaded())

    '''
    test_static = plames_client.request_static("com.inwaiders.plames.rost.test.entity.TestStaticClass")
    test_static.test_static_string = "changed!"
    test_static.push()
    print(test_static.test_static_method())
    '''


def add_hyper_task(runnable):

    hyper = HyperTask()
    hyper.task = runnable

    mutable_data.hyper_tasks_queue.put(hyper)


def __run_hyper_task_cycle():

    while True:
        task = mutable_data.hyper_tasks_queue.get(True)
        __run_hyper_task(task)


def __run_hyper_task(hyper_task):

    mutable_data.environment = Environment()
    mutable_data.environment.init()

    hyper_task.run()

    mutable_data.environment.terminate()

    del mutable_data.environment

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


class HyperTask(object):

    def __init__(self, task=None):
        self.task = task

    def run(self):
        self.task()


class Environment(object):

    def __init__(self):
        self.network_session = NetworkSession()
        self.id = -1

    def init(self):
        answer = plames_client.request(request_packets.RequestCreateEnvironment())
        self.id = answer.environment_id

    def terminate(self):
        self.flush()
        self.network_session.terminate()
        plames_client.request(request_packets.RequestTerminateEnvironment(self.id))

    def flush(self):
        self.network_session.flush()

    def __del__(self):
        del self.network_session


class NetworkSession(object):

    def __init__(self):
        self.object_map = {}

    def terminate(self):
        del self.object_map

    def attach_entity(self, entity):
        s_id = plames_client.request(request_packets.RequestAttachEntity(entity._entity_name, entity.id)).s_id
        self.add_object(entity, s_id)
        return entity

    def add_object(self, object, s_id):
        self.object_map.update({s_id: object})
        object._s_id = s_id
    
    def get_object(self, s_id):
        return self.object_map.get(s_id)

    def is_mapped(self, object):
        
        if hasattr(object, "_s_id"):
            return self.get_object(object._s_id) is not None
        else:
            for s_id in self.object_map:   
                if self.object_map.get(s_id) is object:
                    return True

    def flush(self):

        object_map = self.object_map

        for object_s_id in object_map:
            obj = object_map.get(object_s_id)

            if obj._dirty:
                obj.push()

    def __add_to_dep_map(self, obj, only_dirty, deps):
    
        if hasattr(obj, "__dict__") and hasattr(obj, "_s_id"):
            if obj not in deps:
                if not only_dirty:
                    deps.append(obj)
                elif only_dirty and hasattr(obj, "_dirty") and obj._dirty is True:
                    deps.append(obj)

    def build_dependencies_map(self, obj, only_dirty, dependencies=None):

        if dependencies is None:
            dependencies = []

        if not hasattr(obj, "__dict__"):
            return

        props = obj.__dict__

        for prop_name in props:

            prop = props[prop_name]

            if (type(prop) is list) or (type(prop) is tuple):
                for item in prop:
                    self.__add_to_dep_map(item, only_dirty, dependencies)

            elif type(prop) is dict:
                for item_key in prop:
                    self.__add_to_dep_map(item_key, only_dirty, dependencies)
                    self.__add_to_dep_map(prop[item_key], only_dirty, dependencies)

            else:
                self.__add_to_dep_map(prop, only_dirty, dependencies)
                self.build_dependencies_map(prop, only_dirty, dependencies)

        return dependencies


if __name__ == "__main__":
    main()
