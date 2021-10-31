import requests
import re

from lib.common.abc import Subdomain, Module

from lib import database


class Yahoo(Module):
    """ Search subdomains on Yahoo. """

    def __init__(self, target: str):
        self.target = target
        
    def run(self):
        response = requests.get("https://search.yahoo.com/search?p=site:%s" % self.target)
        
        if response.status_code != 200:
            return

        subdomains = set(re.findall(r"\/\/([a-zA-Z0-9.-]+\.%s)\/" % self.target, response.text))

        for subdomain in subdomains:
            subdomain =  Subdomain(subdomain)

            database.add_subdomain(subdomain)
