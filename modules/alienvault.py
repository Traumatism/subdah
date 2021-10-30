import requests
import re

from lib.common.abc import Module, Subdomain

from lib import database


class AlienVault(Module):

    def __init__(self, target: str):
        self.target = target


    def run(self):
        response = requests.get("https://otx.alienvault.com/api/v1/indicators/domain/%s/passive_dns" % self.target)

        subdomains = set(re.findall(r'\"([a-zA-Z0-9.-]+\.%s)\",' % self.target, response.text))

        for subdomain in subdomains:
            subdomain =  Subdomain(subdomain)

            database.add_subdomain(subdomain)