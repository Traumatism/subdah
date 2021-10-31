import requests

from lib.common.abc import Module, Subdomain

from lib import database


class AlienVault(Module):
    """ Search subdomains on AlienVault. """


    def add_subdomain(self, subdomain: Subdomain):
        """ Add a subdomain to the database. """

        """ 
        Filter things like '*.domain.com', 
        3rd party domains or same as the main domain. 
        """

        if (
            not str(subdomain).endswith(self.target)
            or str(subdomain).startswith("*")
            or str(subdomain) == self.target
        ):
            return

        database.add_subdomain(subdomain)


    def run(self):
        response = requests.get("https://otx.alienvault.com/api/v1/indicators/domain/%s/passive_dns" % self.target)

        if response.status_code != 200:
            return

        json_data = response.json()

        for report in json_data["passive_dns"]:
            self.add_subdomain(Subdomain(report["hostname"]))
