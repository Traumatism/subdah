import requests
import re

from lib.common.abc import Subdomain, Module

from lib import database


class Yahoo(Module):
    """ Search subdomains on Yahoo. """

    def run(self):
        response = requests.get("https://search.yahoo.com/search?p=site:%s" % self.target)
        
        if response.status_code != 200:
            return

        subdomains = set(re.findall(r"\/\/([a-zA-Z0-9.-]+\.%s)\/" % self.target, response.text))

        for subdomain in subdomains:
            database.add_subdomain(Subdomain(subdomain))
