import requests

from lib.common.abc import Module, Subdomain

from lib import database


class Anubis(Module):
    """ Search subdomains in Anubis DB. """

    def run(self):
        response = requests.get(f"https://jonlu.ca/anubis/subdomains/{self.target}")
        
        if response.status_code != 200:
            return

        for subdomain in response.json():
            database.add_subdomain(Subdomain(subdomain))
