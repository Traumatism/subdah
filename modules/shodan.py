import requests
import re

from lib.common.abc import Module, Subdomain

from lib import database


class Shodan(Module):
    """ Search subdomains on Shodan. """


    def run(self):
        response = requests.get("https://shodan.io/domain/%s" % self.target)

        subdomains = set(re.findall(r'<li>([a-zA-Z0-9.-]+)<\/li>\n', response.text))

        for subdomain in subdomains:
            if subdomain in ("*", "SPF"):
                continue

            database.add_subdomain(Subdomain(f"{subdomain}.{self.target}"))
