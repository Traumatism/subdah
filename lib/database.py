from typing import Any

from .logger import Logger
from .common.abc import Subdomain


class Database:
    """ Database class. """

    def __init__(self) -> None:
        self.__subdomains = {}


    @property
    def count(self) -> int:
        """ Return the number of subdomains in the database. """
        return len(self.__subdomains)


    def get_subdomains(self):
        """ Get all subdomains in the database. """
        return self.__subdomains.values()


    def add_subdomain(self, subdomain: Subdomain):
        """ Add a subdomain to the database. """
        if str(subdomain) in map(str, self.__subdomains):
            Logger.debug(f"Subdomain {subdomain} already in database.")
            return

        Logger.debug(f"Adding subdomain {subdomain} to database.")

        self.__subdomains[str(subdomain)] = subdomain


    def update_subdomain(self, subdomain: Subdomain, ip_address: Any):
        """ Update a subdomain in the database. """

        if str(subdomain) not in map(str, self.__subdomains):
            self.add_subdomain(subdomain)

        if ip_address in self.__subdomains[str(subdomain)].resolutions:
            Logger.debug(f"IP address {ip_address} already in database.")
            return

        Logger.debug(f"Updating subdomain {subdomain} in database. (IP address: {ip_address})")

        self.__subdomains[str(subdomain)].resolutions.append(ip_address)
