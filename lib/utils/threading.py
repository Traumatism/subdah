import threading

from ..arguments import arguments


def start_thread(func):
    """ Start a thread with taking care of MAX_THREADS value. """
    while 1:
        if threading.active_count() <= arguments.threads:
            return threading.Thread(target=func).start()


def wait_for_threads_to_stop():
    """ Wait for all started threads to finish. """
    while 1:
        if threading.active_count() == 1:
            return