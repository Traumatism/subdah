import requests
import re

from lib.common.abc import Module, Subdomain

from lib.config import BASE_REGEX, USER_AGENT

from lib import database


class Google(Module):
    """ Search subdomains on Google. """
    
    def run(self):
        response = requests.get(
            "https://www.google.com/search?q=site:%(target)s+-www&oq=site:%(target)s+-www&uact=5"
            % {"target": self.target},
            headers={
                "User-Agent": USER_AGENT
            }
        )

        subdomains = set(re.findall(BASE_REGEX % self.target, response.text))

        for subdomain in subdomains:
           database.add_subdomain(Subdomain(subdomain))
