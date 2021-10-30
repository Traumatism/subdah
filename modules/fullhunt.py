import requests
import re

from lib.common.abc import Module, Subdomain

from lib import database


class FullHunt(Module):

    def __init__(self, target: str):
        self.target = target


    def run(self):
        response = requests.get("https://fullhunt.io/search?query=%s" % self.target)

        subdomains = set(re.findall(r'\/host\/([a-zA-Z0-9.-]+\.%s)\"' % self.target, response.text))

        for subdomain in subdomains:
            subdomain =  Subdomain(subdomain)

            database.add_subdomain(subdomain)
