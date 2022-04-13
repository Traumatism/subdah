import requests

from ..abc import Enumerator
from ..types import Subdomain


class AnubisDB(Enumerator):

    engine = "AnubisDB"

    def scan(self, target: str):
        response = requests.get(
            f"https://jonlu.ca/anubis/subdomains/{target}"
        )

        return map(Subdomain, response.json())
