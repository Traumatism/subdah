import dns.resolver
import requests

from abc import ABC, abstractmethod

from lib.arguments import arguments

""" Disable SSL warning. """
from requests.packages import urllib3
from urllib3.exceptions import InsecureRequestWarning


urllib3.disable_warnings(
    category=InsecureRequestWarning
)

class Subdomain(ABC):
    """ Abstract base class for all subdomains. """

    def __init__(self, subdomain: str) -> None:

        self.__subdomain = subdomain.lower()

        self.resolutions = []
        
        self.http_banner = None

        super().__init__()

    def gather_http_banner(self) -> None | bool | str:
        """ Gather HTTP banner if an HTTP server is running. """

        if self.http_banner is not None:
            return

        try:
            response = requests.get(
                f"http://{self.__subdomain}:80", 
                verify=False, timeout=arguments.http_timeout / 1000
            )

            self.http_banner = response.headers['Server']

        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, requests.exceptions.TooManyRedirects):
            self.http_banner = "n/a"
        except (KeyError, ValueError):
            self.http_banner = "HTTP server"

        return self.http_banner

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

