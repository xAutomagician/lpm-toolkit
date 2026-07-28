from app.dataset import load_prefix_infos, range_to_cidrs
from app.repository import PyTriciaPrefixRepository


def test_range_to_cidrs_returns_minimal_prefixes():
    assert range_to_cidrs("185.10.148.0", "185.10.151.255") == [
        "185.10.148.0/22"
    ]


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
