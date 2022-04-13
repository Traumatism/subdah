import requests

from ..abc import Enumerator
from ..types import Subdomain


class CrtSh(Enumerator):

    engine = "crt.sh"

    def scan(self, target: str):
        response = requests.get(f"https://crt.sh?q={target}&output=json")

        for report in response.json():
            optional = report["name_value"]

            if "\n" in optional:
                yield from map(Subdomain, optional.split("\n"))
            else:
                yield Subdomain(optional)
