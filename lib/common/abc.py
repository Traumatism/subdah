import dns.resolver
import requests

from abc import ABC, abstractmethod

""" List of common ports """
PORTS = (
    21,    # FTP
    22,    # SSH
    80,    # HTTP
    443,   # HTTPS
    3306,  # MySQL
    3389,  # RDP
    25565, # Minecraft
    27017, # MongoDB
)


class Subdomain(ABC):
    """ Abstract base class for all subdomains. """

    def __init__(self, subdomain: str) -> None:

        self.__subdomain = subdomain.lower()

        self.resolutions = []
        
        self.open_ports = []

        super().__init__()


    def banner(self) -> str:
        """ Gather HTTP banner if an HTTP server is running. """


    @property
    def resolvable(self) -> bool:
        """ Know if the subdomain is resolvable or not.

        Returns:
            bool: True if the subdomain is resolvable, False otherwise.
        """

        try:
            dns.resolver.query(self.__subdomain, 'A')
            return True
        except:
            return False


    def scan_ports(self, ports=[22, 80, 443, 3306, 3389, 27017]):
        """ Scan the subdomain for open ports. """
        if self.resolvable is False:
            return


    def resolve(self) -> None | list:
        """ Resolve the subdomain.

        Returns:
            None | list: If the subdomain is not resolvable, return None.
        """
        
        return None if self.resolvable is False else [x.address for x in dns.resolver.query(self.__subdomain, 'A')]


    def __str__(self) -> str:
        """ Return the subdomain. """
        return self.__subdomain


class Module(ABC):
    """ Abstract base class for all modules. """

    def __init__(self, target: str):
        """ Initialize the module.

        Args:
            target (str): Target to scan.
        """
        self.target = target


    @abstractmethod
    def run(self):
        """ Run the module. """
        pass
