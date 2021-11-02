import requests
import re

from lib.common.abc import Module, Subdomain

from lib import database
from lib.config import BASE_REGEX


class Hackertarget(Module):
    """ Search subdomains Hackertarget. """


    def run(self):
        response = requests.get("https://api.hackertarget.com/hostsearch?q=%s" % self.target)

        subdomains = re.findall(r'%s,[\d\.]+\n' % BASE_REGEX % self.target, response.text)

        for subdomain in subdomains:
            database.add_subdomain(Subdomain(subdomain))
