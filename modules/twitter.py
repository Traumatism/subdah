import requests
import re

from lib.common.abc import Module, Subdomain

from lib.config import USER_AGENT, BASE_REGEX

from lib import database

COUNT = 500


class Twitter(Module):
    """ Search subdomains on Twitter. """

    def run(self):
        headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'user-agent': USER_AGENT
        }

        response = requests.get(
            'https://api.twitter.com/1.1/search/tweets.json', 
            headers=headers, 
            params={
                "q": self.target,
                "count": COUNT
            }
        )

        content = str(response.text) # lazy to parse this json lol

        subdomains = set(re.findall(BASE_REGEX % self.target, content))

        for subdomain in subdomains:
           database.add_subdomain(Subdomain(subdomain))
