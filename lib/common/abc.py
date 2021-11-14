import dns.resolver
import requests

from typing import (
    List, Text, Union
)

from abc import (
    ABC, abstractmethod
)

from ..arguments import arguments

""" Disable SSL warning. """
from requests.packages import urllib3
from urllib3.exceptions import InsecureRequestWarning


urllib3.disable_warnings(
    category=InsecureRequestWarning
)

class Subdomain(ABC):
    """ Abstract base class for all subdomains. """


    def __init__(self, subdomain: Text) -> None:

        self.__subdomain = subdomain.lower()

        self.resolutions = []

        self.http_server = None

        super().__init__()


    def grab_http_server(self) -> Union[None, Text]:
        """ Grab HTTP server if an HTTP server is running. """

        if self.http_server is not None:
            return

        try:
            response = requests.get(
                f"http://{self.__subdomain}:80", 
                verify=False, timeout=arguments.http_timeout / 1000
            )

            self.http_server = response.headers['Server']

        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, requests.exceptions.TooManyRedirects):
            self.http_server = "n/a"
        except (KeyError, ValueError):
            self.http_server = "HTTP server"

        return self.server


    @property
    def resolvable(self) -> bool:
        """ Know if the subdomain is resolvable or not. """

        try:
            dns.resolver.query(self.__subdomain, 'A')
            return True
        except:
            return False


    @property
    def domain(self) -> str:
        """ Return the domain. """

        return ".".join(self.__subdomain.split('.')[-2:])
    


    def resolve(self) -> Union[None, List[Text]]:
        """ Resolve the subdomain. """

        return None if self.resolvable is False else [x.address for x in dns.resolver.query(self.__subdomain, 'A')]


    def __str__(self) -> Text:
        """ Return the subdomain. """

        return self.__subdomain


class Module(ABC):
    """ Abstract base class for all modules. """

    def __init__(self, target: Text):
        """ Initialize the module.

        Args:
            target (str): Target to scan.
        """

        self.target = target


    @abstractmethod
    def run(self):
        """ Run the module. """

