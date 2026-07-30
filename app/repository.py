import ipaddress
import os
from abc import ABC, abstractmethod
from dataclasses import replace
from pathlib import Path

import pytricia

from app.dataset import IPTOASN_V4_URL, ensure_dataset, load_prefix_infos
from app.domain import PrefixInfo


DEFAULT_DATASET_PATH = Path("data/ip2asn-v4.tsv.gz")


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


class PyTriciaPrefixRepository(IPrefixRepository):
    def __init__(self) -> None:
        self._tree = pytricia.PyTricia(32)
        self.prefix_count = 0

    def add(self, info: PrefixInfo) -> None:
        network = ipaddress.ip_network(info.prefix, strict=False)
        if network.version != 4:
            raise ValueError(f"Only IPv4 prefixes are supported: {info.prefix}")

        prefix = str(network)
        self._tree[prefix] = replace(info, prefix=prefix)
        self.prefix_count += 1

    def get(self, ip: str) -> PrefixInfo | None:
        address = ipaddress.ip_address(ip)
        if address.version != 4:
            return None

        try:
            return self._tree[str(address)]
        except KeyError:
            return None


def build_prefix_repository() -> IPrefixRepository:
    dataset_path = Path(os.getenv("IPTOASN_DATASET_PATH", str(DEFAULT_DATASET_PATH)))
    dataset_url = os.getenv("IPTOASN_DATASET_URL", IPTOASN_V4_URL)
    timeout = float(os.getenv("IPTOASN_DOWNLOAD_TIMEOUT", "30"))

    dataset_path = ensure_dataset(
        dest_path=dataset_path,
        url=dataset_url,
        timeout=timeout,
    )

    repository = PyTriciaPrefixRepository()
    for prefix_info in load_prefix_infos(dataset_path):
        repository.add(prefix_info)

    return repository
