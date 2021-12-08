"""Module to manage threads """

import threading

from ..logger import Logger
from ..arguments import arguments


def start_thread(func):
    """ Start a new thread """
    while True:
        if threading.active_count() <= arguments.threads:
            return threading.Thread(target=func).start()


def start_module_thread(module):
    """ Start a module thread """
    Logger.debug(f"Running module: {module}...")
    start_thread(module._run)


def wait_for_threads_to_stop():
    """ Wait for all started threads to finish. """
    while 1:
        if threading.active_count() == 2:
            return

