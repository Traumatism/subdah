import requests

from lib.common.abc import Module, Subdomain

from lib import database


class ThreatCrowd(Module):
    """ Search subdomains on ThreatCrowd. """


    def run(self):
        response = requests.get("https://www.threatcrowd.org/searchApi/v2/domain/report/?domain=%s" % self.target)

        json_data = response.json()

        if json_data["response_code"] == "0":
            return

        subdomains = response.json()["subdomains"]

        for subdomain in subdomains:
            database.add_subdomain(Subdomain(subdomain))
