from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class PrefixInfo:
    prefix: str
    asn: int
    country: str | None
    description: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PrefixRange:
    start_ip: str
    end_ip: str
    asn: int
    country: str | None
    description: str
