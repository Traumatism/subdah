import requests
import re

from lib.common.abc import Module, Subdomain

from lib import database


class Hackertarget(Module):
    """ Search subdomains Hackertarget. """

    def __init__(self, target: str):
        self.target = target


    def run(self):
        response = requests.get("https://api.hackertarget.com/hostsearch?q=%s" % self.target)

        subdomains = re.findall(r'([a-zA-Z0-9.-]+\.%s),[\d\.]+\n' % self.target, response.text)

        for subdomain in subdomains:
            subdomain =  Subdomain(subdomain)

            database.add_subdomain(subdomain)
