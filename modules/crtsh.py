import requests
import re

from lib.common.abc import Module, Subdomain

from lib import database


class CRTSh(Module):
    """ Search subdomains on crt.sh. """

    def add_subdomain(self, subdomain: Subdomain):
        """ Add a subdomain to the database. """
        
        """ 
        Filter things like '*.domain.com', 
        3rd party domains or same as the main domain. 
        """
        
        if (
            not str(subdomain).endswith(self.target)
            or str(subdomain).startswith("*")
            or str(subdomain) == self.target
        ):
            return

        database.add_subdomain(subdomain)

    def run(self):
        response = requests.get("https://crt.sh?q=%s&output=json" % self.target)

        json_data = response.json()

        for report in json_data:
            subdomain = Subdomain(report["name_value"])
            
            if "\n" in str(subdomain):
                parts = str(subdomain).split("\n")
                
                for part in parts:
                    self.add_subdomain(Subdomain(part))
                    
                continue
            
            self.add_subdomain(subdomain)