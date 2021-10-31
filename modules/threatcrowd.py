import requests

from lib.common.abc import Module, Subdomain

from lib import database


class ThreatCrowd(Module):
    """ Search subdomains on ThreatCrowd. """

    def __init__(self, target: str):
        self.target = target


    def run(self):
        response = requests.get("https://www.threatcrowd.org/searchApi/v2/domain/report/?domain=%s" % self.target)

        json_data = response.json()

        if json_data["response_code"] == "0":
            return

        subdomains = response.json()["subdomains"]

        for subdomain in subdomains:
            subdomain =  Subdomain(subdomain)

            database.add_subdomain(subdomain)