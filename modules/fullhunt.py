import requests
import re

from lib.common.abc import Module, Subdomain

from lib import database


class FullHunt(Module):
    """ Search subdomains on FullHunt. """


    def run(self):
        response = requests.get("https://fullhunt.io/api/v1/domain/%s/subdomains" % self.target)

        if response.status_code != 200:
            return

        json_data = response.json()

        for subdomain in json_data["hosts"]:
            database.add_subdomain(Subdomain(subdomain))
