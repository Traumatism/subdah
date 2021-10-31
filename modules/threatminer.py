import requests

from lib.common.abc import Module, Subdomain

from lib import database


class ThreatMiner(Module):
    """ Search subdomains on ThreatMiner. """


    def run(self):
        response = requests.get("https://api.threatminer.org/v2/domain.php?q=%s&rt=5" % self.target)

        subdomains = response.json()["results"]

        for subdomain in subdomains:
            database.add_subdomain(Subdomain(subdomain))
