from . import (console, __version__)


BANNER = r"""
[cyan bold]
              _           _        _     
   ____ ,   . \ ___    ___/   ___  /     
  (     |   | |/   \  /   |  /   ` |,---.
  `--.  |   | |    ` ,'   | |    | |'   `
 \___.' `._/| `___,' `___,' `.__/| /    |
                          `              
  [white bold]Subdah v%s  --  cool subdomains scanner[/white bold]
  @ [red bold]github.com/traumatism/subdah[/red bold]
[/cyan bold]

"""


def print_banner():
    """ Print the banner to the terminal. """
    console.print(BANNER % __version__)

