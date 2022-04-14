from abc import ABC, abstractmethod
from typing import Iterable, Type

from .types import Subdomain

__all__ = ("Enumerator", "EnumeratorType")

EnumeratorType = Type["Enumerator"]


class Enumerator(ABC):
    """ Abstract class for each subdomains enumerator """

    engine: str

    def __init__(self) -> None:
        if not self.engine:
            raise ValueError("Engine name not set")

        super().__init__()

    @abstractmethod
    def scan(self, target: str) -> Iterable[Subdomain]:
        """ Scan target and return all the results """
        raise NotImplementedError()
