__version__ = "2.0.0"

from .database import Database
from .logger import Logger, console

database = Database()  # database containing all subdomains.
