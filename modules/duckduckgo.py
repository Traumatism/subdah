import requests
import re

from lib.common.abc import Module, Subdomain

from lib.config import BASE_REGEX, USER_AGENT

from lib import database


class DuckDuckGo(Module):
    """ Search subdomains on DuckDuckGo. """
    
    def run(self):
        response = requests.get(
            "https://duckduckgo.com/html/?q=site:%s" % self.target,
            headers={"User-Agent": USER_AGENT}
        )

        subdomains = set(re.findall(BASE_REGEX % self.target, response.text.lower()))

        for subdomain in subdomains:
           database.add_subdomain(Subdomain(subdomain))
