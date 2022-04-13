import functools
import socket

from typing import NamedTuple, Optional, Type

SubdomainType = Type['Subdomain']


class Subdomain(NamedTuple):
    """ Subdomain type """

    subdomain: str

    def __str__(self):
        return self.subdomain

    def as_json(self):
        """ Return subdomain as json """
        return {
            "host": self.subdomain,
            "ip": self.ip_address(),
        }

    @functools.lru_cache(maxsize=1)
    def ip_address(self) -> Optional[str]:
        """ Get the IP address of a subdomain """
        try:
            return socket.gethostbyname(self.subdomain)
        except socket.gaierror:
            return
