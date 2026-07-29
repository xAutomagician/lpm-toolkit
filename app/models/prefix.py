from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class PrefixInfo:
    asn: int
    country: str
    description: str
    prefix: str  # the actual matched CIDR block, e.g. "1.1.1.0/24"

    def to_dict(self) -> dict:
        return asdict(self)
