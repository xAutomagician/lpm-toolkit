
from abc import ABC, abstractmethod

from app.models.prefix import PrefixInfo
from app.repository.base import Repository


class IPrefixRepository(ABC, Repository):
    @abstractmethod
    async def create(self, ip) -> PrefixInfo:
        pass

    @abstractmethod
    async def read(self, ip) -> PrefixInfo:
        pass

    @abstractmethod
    async def update(self, ip) -> PrefixInfo:
        pass

    @abstractmethod
    async def delete(self, ip) -> PrefixInfo:
        pass
