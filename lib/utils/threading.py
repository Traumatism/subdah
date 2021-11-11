import threading

from lib.logger import Logger

from ..arguments import arguments


def start_module_thread(module):
    """ Start a thread with taking care of threads value. """

    while 1:
        if threading.active_count() <= arguments.threads:
            return all((
                Logger.debug(f"Running module: {module}"), 
                threading.Thread(target=module.run).start()
            )) or None


def wait_for_threads_to_stop():
    """ Wait for all started threads to finish. """

    while 1:
        if threading.active_count() == 1:
            return
