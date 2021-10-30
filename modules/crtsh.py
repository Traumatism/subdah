import requests
import re

from lib.common.abc import Module, Subdomain

from lib import database


class CRTSh(Module):

    def __init__(self, target: str):
        self.target = target


    def run(self):
        response = requests.get("https://crt.sh?q=%s&output=json" % self.target)

        subdomains = set(re.findall(r'\"([a-zA-Z0-9.-]+\.%s)\"' % self.target, response.text))

        for subdomain in subdomains:
            subdomain =  Subdomain(subdomain)

            database.add_subdomain(subdomain)
