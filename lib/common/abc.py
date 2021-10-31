import dns.resolver

from abc import ABC, abstractmethod


class Subdomain(ABC):
    """ Abstract base class for all subdomains. """

    def __init__(self, subdomain: str) -> None:

        self.__subdomain = subdomain

        self.resolutions = []

        super().__init__()


    @property
    def resolvable(self) -> bool:
        """ Return True if the subdomain is resolvable. """
        try:
            dns.resolver.query(self.__subdomain, 'A')
            return True
        except:
            return False


    def resolve(self) -> None | list:
        """ Resolve the subdomain. """
        return None if self.resolvable is False else [x.address for x in dns.resolver.query(self.__subdomain, 'A')]


    def __str__(self) -> str:
        """ Return the subdomain. """
        return self.__subdomain


class Module(ABC):
    """ Abstract base class for all modules. """

    def __init__(self, target: str):
        """ Initialize the module. """
        self.target = target


    @abstractmethod
    def run(self):
        """ Run the module. """
        pass