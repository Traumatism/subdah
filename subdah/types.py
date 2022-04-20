from typing import Dict, NamedTuple, Optional, Type
from subdah.utils import internetdb, resolve

__all__ = ("Subdomain", "SubdomainType")

SubdomainType = Type["Subdomain"]


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
            "shodan": self.internetdb()
        }

    def ip_address(self) -> Optional[str]:
        """ Get the IP address of a subdomain """
        return resolve(self.subdomain)

    def internetdb(self) -> Dict:
        """ Get the InternetDB data of a subdomain """
        ip_address = self.ip_address()

        return internetdb(ip_address) if ip_address else {}
