import threadz  # using my own libraries? yeah

from rich.console import Console

from typing import Callable, Iterable, List, Generator

from .scanners.alienvault import AlienVault
from .scanners.anubisdb import AnubisDB
from .scanners.crtsh import CrtSh
from .scanners.fullhunt import FullHunt

from .types import Subdomain
from .abc import Enumerator, EnumeratorType


class Scanner:
    """ Scanner class """

    def __init__(
        self,
        target: str,
        verbose: bool = False,
        console: Console = Console(),
    ) -> None:

        self.target = target
        self.verbose = verbose
        self.console = console

        self.enumerators: List[EnumeratorType] = [
            AlienVault,
            AnubisDB,
            CrtSh,
            FullHunt,
        ]

        self.subdomains: List[Subdomain] = []

    def runner(self, enumerator: Enumerator) -> Callable[..., Iterable[Subdomain]]:
        """ Decorator for the scan method """

        def scan() -> Iterable[Subdomain]:
            """ Scan target and return all the results """

            if self.verbose:
                self.console.log(f"Running {enumerator.engine}...")

            return enumerator.scan(self.target)

        return scan

    def scan(self, concurrency=10) -> Iterable[Subdomain]:
        """ Scan target and return all the results """
        tasks = [
            (self.runner(enumerator), tuple(), {})
            for enumerator in
            map(lambda cls: cls(), self.enumerators)
        ]

        for idx, subdomains in threadz.gather(tasks, concurrency).items():

            if isinstance(subdomains, Exception):
                exc = subdomains

                if self.verbose:
                    self.console.log(f"{self.enumerators[idx]} returned an exception: {exc}")

                continue

            self.subdomains.extend(subdomains)

        return set(self.subdomains)
