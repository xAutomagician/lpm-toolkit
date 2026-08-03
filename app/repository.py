from abc import ABC, abstractmethod
from collections.abc import Iterator

import pytricia

from app.schemas import PrefixInfo


class Repository:
    def add(self, data):
        raise NotImplementedError

    def get(self, id):
        raise NotImplementedError

    def update(self, id, data):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError


class IPrefixRepository(ABC, Repository):
    @abstractmethod
    def add(self, prefix: PrefixInfo) -> None:
        pass

    @abstractmethod
    def get(self, ip: str) -> PrefixInfo | None:
        pass


class InMemoryPrefixRepository(IPrefixRepository):
    def __init__(self) -> None:
        self._tree = pytricia.PyTricia(32)

    def add(self, prefix: PrefixInfo) -> None:
        self._tree[str(prefix.prefix)] = prefix

    def get(self, ip: str) -> PrefixInfo | None:
        prefix_info = self._tree[ip]
        if prefix_info:
            return prefix_info

    def load(self, infos: Iterator[PrefixInfo]) -> None:
        for info in infos:
            self.add(info)
