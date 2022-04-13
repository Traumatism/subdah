import requests

from ..abc import Enumerator
from ..types import Subdomain


class AlienVault(Enumerator):

    engine = "AlienVault"

    def scan(self, target: str):
        response = requests.get(
            f"https://otx.alienvault.com/api/v1/indicators/domain/{target}/passive_dns"
        )

        return map(
            lambda x: Subdomain(x["hostname"]),
            response.json()["passive_dns"]
        )
