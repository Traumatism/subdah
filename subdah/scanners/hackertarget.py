import requests

from ..abc import Enumerator
from ..types import Subdomain


class HackerTarget(Enumerator):

    engine = "HackerTarget"

    def scan(self, target: str):
        response = requests.get(
            f"https://api.hackertarget.com/hostsearch/?q={target}"
        )

        return map(
            Subdomain,
            map(lambda x: x.split(",")[0], response.text.split("\n"))
        )
