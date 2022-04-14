import socket
import requests
import functools
import contextlib

from rich.table import Table
from typing import Dict, Optional

from . import CACHE_SIZE


@functools.lru_cache(maxsize=CACHE_SIZE)
def internetdb(ip_address: str) -> Dict:
    """ Get the InternetDB data of a subdomain """
    return (requests.get(
        f"https://internetdb.shodan.io/{ip_address}"
    )).json()


@functools.lru_cache(maxsize=CACHE_SIZE)
def resolve(hostname: str) -> Optional[str]:
    """ Get the IP address of a subdomain """
    with contextlib.suppress(socket.gaierror):
        return socket.gethostbyname(hostname)


def json_to_rich_table(json_data: Dict) -> Table:
    """ Convert JSON data to a rich table """
    table = Table(show_header=False)

    for key, value in json_data.items():
        if not value:
            continue

        if isinstance(value, list):
            table.add_row(key, ", ".join(map(str, value)))
        else:
            table.add_row(key, value)

    return table
