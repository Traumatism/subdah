import socket
import requests
import functools
import contextlib

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
