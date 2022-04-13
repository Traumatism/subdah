import requests

from ..abc import Enumerator
from ..types import Subdomain


class FullHunt(Enumerator):

    engine = "FullHunt"

    def scan(self, target: str):
        response = requests.get(
            f"https://fullhunt.io/api/v1/domain/{target}/subdomains"
        )

        return map(Subdomain, response.json()["hosts"])
