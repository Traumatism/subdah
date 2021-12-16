import requests
import re

from lib.common.abc import Module, Subdomain
from lib.config import BASE_REGEX
from lib import database


class ThreatCrowd(Module):
    """ Search subdomains on ThreatCrowd. """

    def run(self):
        response = requests.get("https://www.threatcrowd.org/searchApi/v2/domain/report/?domain=%s" % self.target)

        subdomains = set(re.findall(BASE_REGEX % self.target, response.text))
        for subdomain in subdomains:
            database.add_subdomain(Subdomain(subdomain))
