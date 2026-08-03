from ipaddress import IPv4Address, IPv4Network

from pydantic import BaseModel


class PrefixInfo(BaseModel):
    prefix: IPv4Network
    asn: int
    country: str | None
    description: str


class PrefixRange(BaseModel):
    start_ip: IPv4Address
    end_ip: IPv4Address
    asn: int
    country: str | None
    description: str
