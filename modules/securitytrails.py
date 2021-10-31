import requests
import re


from lib.common.abc import Module, Subdomain

from lib import database


class SecurityTrails(Module):
    """ Search subdomains on SecurityTrails. """

    def __init__(self, target: str):
        super().__init__(target)
        
        
    def run(self):
        response = requests.get(
            "https://securitytrails.com/list/keyword/%s" % self.target,
            headers={"Content-Type": "application/json"}
        )
        
        subdomains = set(re.findall(r'\"([a-zA-Z0-9.-]+\.%s)\"' % self.target, response.text))

        for subdomain in subdomains:

            subdomain =  Subdomain(subdomain)

            database.add_subdomain(subdomain)
