from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class SubnetInfo:
    cidr: str
    network_address: str
    broadcast_address: Optional[str]
    netmask: str
    wildcard_mask: str
    num_addresses: int
    num_usable_hosts: int
    first_usable_host: Optional[str]
    last_usable_host: Optional[str]
    is_private: bool
    version: int

    def to_dict(self) -> dict:
        return asdict(self)
