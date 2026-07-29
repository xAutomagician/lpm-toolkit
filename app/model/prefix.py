from dataclasses import dataclass


class InvalidIPError(ValueError):
    pass


@dataclass(frozen=True)
class Prefix:
    asn: int
    country: str
    description: str
    prefix: str  # the actual matched CIDR block, e.g. "1.1.1.0/24"
