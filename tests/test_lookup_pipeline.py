from ipaddress import IPv4Address

import pytest
from fastapi import HTTPException

from app.api.v1.lookup import get_ip_lookup
from app.dataset import load_prefix_infos, range_to_cidrs
from app.repository import PyTriciaPrefixRepository
from app.schemas import PrefixInfo


class FakePrefixRepository:
    def __init__(self, result: PrefixInfo | None) -> None:
        self.result = result
        self.requested_ip = None

    def get(self, ip: str) -> PrefixInfo | None:
        self.requested_ip = ip
        return self.result


def test_range_to_cidrs_returns_minimal_prefixes():
    assert range_to_cidrs("185.10.148.0", "185.10.151.255") == ["185.10.148.0/22"]


def test_repository_gets_prefix_info_from_tsv(tmp_path):
    dataset_path = tmp_path / "ip2asn-v4.tsv"
    dataset_path.write_text(
        "\n".join(
            [
                "185.10.146.0\t185.10.147.255\t0\tNone\tNot routed",
                "185.10.148.0\t185.10.151.255\t197558\tDE\tMUTH",
            ]
        ),
        encoding="utf-8",
    )

    repository = PyTriciaPrefixRepository()
    for prefix_info in load_prefix_infos(dataset_path):
        repository.add(prefix_info)

    routed = repository.get("185.10.149.1")
    assert routed is not None
    assert routed.prefix == "185.10.148.0/22"
    assert routed.asn == 197558
    assert routed.country == "DE"
    assert routed.description == "MUTH"

    not_routed = repository.get("185.10.146.1")
    assert not_routed is not None
    assert not_routed.prefix == "185.10.146.0/23"
    assert not_routed.asn == 0
    assert not_routed.country is None
    assert not_routed.description == "Not routed"

    assert repository.get("8.8.8.8") is None


def test_lookup_endpoint_returns_prefix_model():
    prefix_info = PrefixInfo(
        prefix="8.8.8.0/24",
        asn=15169,
        country="US",
        description="GOOGLE",
    )
    repository = FakePrefixRepository(prefix_info)

    result = get_ip_lookup(IPv4Address("8.8.8.8"), repository)

    assert result == prefix_info
    assert repository.requested_ip == "8.8.8.8"


def test_lookup_endpoint_returns_404_for_missing_prefix():
    repository = FakePrefixRepository(None)

    with pytest.raises(HTTPException) as exc_info:
        get_ip_lookup(IPv4Address("8.8.8.8"), repository)

    assert exc_info.value.status_code == 404
