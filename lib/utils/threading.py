"""
Module to manage threads.
"""

import threading

from ..logger import Logger
from ..arguments import arguments


def start_thread(func):
    """
    Start a new thread

    Args:
        func (function): Function to start a thread for.
    """

    while True:
        if threading.active_count() <= arguments.threads:
            return threading.Thread(target=func).start()


def start_module_thread(module):
    """ 
    Start a thread for a module.
    
    Args:
        module (Module): Module to start a thread for.
    """
    Logger.debug(f"Running module: {module}...")

    start_thread(module.run)


def wait_for_threads_to_stop():
    """ Wait for all started threads to finish. """

    while 1:
        if threading.active_count() == 2:
            return
