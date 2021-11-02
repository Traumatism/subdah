import requests
import re

from lib.common.abc import Module, Subdomain

from lib.config import BASE_REGEX, USER_AGENT

from lib import database


class Google(Module):
    """ Search subdomains on Google. """
    
    
    def run(self):
        #https://www.google.com/search?q=site%3Arinaorc.com+-www&ei=hx-BYeSvOoGWaLHJofgB&oq=site%3Arinaorc.com+-www&gs_lcp=Cgdnd3Mtd2l6EANKBAhBGAFQAFgAYLiJDGgHcAB4AIABAIgBAJIBAJgBAMABAQ&sclient=gws-wiz&ved=0ahUKEwikj4GbyPnzAhUBCxoKHbFkCB8Q4dUDCA4&uact=5
        
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
