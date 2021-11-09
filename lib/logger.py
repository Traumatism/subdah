from rich.console import Console

from .arguments import arguments

class Logger:
    """ Logger class. """

    console = Console(log_time_format="<%X>")

    @classmethod
    def display_dict(cls, dictionnary: dict):
        """ Display a dictionnary as fancy as possible. """
        cls.console.print("".join(
            "[green]*[/green] %s%s: %s\n"
            % (key, " " * (max(len(k) for k in dictionnary) - len(key) + 2), value)
            for key, value in dictionnary.items()
        )[:-1])

    @classmethod
    def info(cls, message):
        """ Log info message. """
        cls.console.print(message, style="bold cyan")

    @classmethod
    def warning(cls, message):
        """ Log warning message. """
        cls.console.print(message, style="bold yellow")

    @classmethod
    def error(cls, message):
        """ Log error message. """
        cls.console.print(message, style="bold red")

    @classmethod
    def success(cls, message):
        """ Log success message. """
        cls.console.print(message, style="bold green")

    @classmethod
    def debug(cls, message):
        """ Log debug message. """
        if arguments.debug is True:
            cls.console.print(message, style="bold magenta")
