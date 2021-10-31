import requests

from lib.common.abc import Module, Subdomain

from lib import database


class ThreatMiner(Module):
    """ Search subdomains on ThreatMiner. """

    def __init__(self, target: str):
        self.target = target


    def run(self):
        response = requests.get("https://api.threatminer.org/v2/domain.php?q=%s&rt=5" % self.target)

        subdomains = response.json()["results"]

        for subdomain in subdomains:
            subdomain =  Subdomain(subdomain)

            database.add_subdomain(subdomain)
