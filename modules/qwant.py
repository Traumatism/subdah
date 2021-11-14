OFFSETS = (10, 20, 30, 40)
LOCALE = "fr_FR"

import requests
import re

from lib.common.abc import Module, Subdomain

from lib.config import BASE_REGEX, USER_AGENT

from lib import database


class Qwant(Module):
    """ Search subdomains on Qwant. """

    def run(self):

        for offset in OFFSETS: # range(10, 50, 10)
            response = requests.get(
                "https://api.qwant.com/v3/search/web?q=site:%s&count=10&locale=%s&offset=%d"
                % (self.target, LOCALE, offset),
                headers={"User-Agent": USER_AGENT}
            )

            subdomains = set(re.findall(BASE_REGEX % self.target, response.text.lower()))

            for subdomain in subdomains:
                database.add_subdomain(Subdomain(subdomain))
