from typing import Optional

from app.models.prefix import PrefixInfo
from app.repository.prefix import IPrefixRepository


class LookupService:
    def __init__(self, prefix_repository: Optional[IPrefixRepository] = None):
        self.prefix_repository = prefix_repository

    def lookup_ip(self, ip: str) -> Optional[PrefixInfo]:
        """Offline lookup"""
        if self.asn_repository is None:
            raise
        return self.asn_repository.lookup(ip)
