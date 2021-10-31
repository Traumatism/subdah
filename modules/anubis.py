import requests

from lib.common.abc import Module, Subdomain

from lib import database


class Anubis(Module):
    """ Search subdomains in Anubis DB. """
    
    def __init__(self, target: str):
        super().__init__(target)
        
    
    def run(self):
        response = requests.get(f"https://jonlu.ca/anubis/subdomains/{self.target}")
        
        if response.status_code != 200:
            return
        
        subdomains = response.json()
        
        for subdomain in subdomains:
            subdomain =  Subdomain(subdomain)

            database.add_subdomain(subdomain)
