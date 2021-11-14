from .arguments import arguments

from .config import (
    INFO_COLOR, WARN_COLOR, SUCCESS_COLOR,
    ERROR_COLOR, DEBUG_COLOR
)

from rich.console import Console

console = Console(log_time_format="(%X)") # console to use for printing.


class Logger:
    """ Logger Module. """


    @staticmethod
    def info(message):
        """ Log an information message.

        Args:
            message ([type]): Message to log.
        """

        console.log(message, style=INFO_COLOR)


    @staticmethod
    def warning(message):
        """ Log a warn message.

        Args:
            message ([type]): Message to log.
        """
        console.log(message, style=WARN_COLOR)


    @staticmethod
    def error(message):
        """ Log an error message.

        Args:
            message ([type]): Message to log.
        """
        console.log(message, style=ERROR_COLOR)


    @staticmethod
    def success(message):
        """ Log a success message.

        Args:
            message ([type]): Message to log.
        """
        console.log(message, style=SUCCESS_COLOR)


    @staticmethod
    def debug(message):
        """ Log a debug message.

        Args:
            message ([type]): Message to log.
        """
        if arguments.debug is True:
            console.log(message, style=DEBUG_COLOR)
