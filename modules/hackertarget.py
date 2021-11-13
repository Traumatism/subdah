import requests
import re

from lib.common.abc import Module, Subdomain

from lib import database
from lib.config import BASE_REGEX


class Hackertarget(Module):
    """ Search subdomains Hackertarget. """

    def run(self):
        response = requests.get("https://api.hackertarget.com/hostsearch?q=%s" % self.target)

        subdomains = re.findall(r'(%s),([\d\.]+)+\n' % BASE_REGEX % self.target, response.text)

        for subdomain, ip_addr in subdomains:
            subdomain = Subdomain(subdomain)

            database.add_subdomain(subdomain)
            
            database.update_subdomain(subdomain, ip_addr)
