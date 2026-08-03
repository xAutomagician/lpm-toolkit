import csv
import gzip
import io
import ipaddress
from contextlib import contextmanager
from typing import TextIO

import requests

from app.schemas import PrefixInfo

IPTOASN_V4_URL = "https://github.com/pl-strflt/iptoasn/raw/main/data/ip2asn-v4.tsv.gz"


@contextmanager
def open_tsv_stream(url: str, timeout: int):
    with requests.get(url, timeout=timeout, stream=True) as r:
        r.raise_for_status()
        with gzip.GzipFile(fileobj=r.raw) as gz:
            yield io.TextIOWrapper(gz, encoding="utf-8")


def parse_tsv_rows(tsv_stream: TextIO):
    yield from csv.reader(tsv_stream, delimiter="\t")


def get_dataset(url: str = IPTOASN_V4_URL, timeout: int = 15):
    with open_tsv_stream(url, timeout=timeout) as tsv_stream:
        yield from parse_tsv_rows(tsv_stream)


def range_to_cidrs(first: str, last: str) -> list[str]:
    first_ip = ipaddress.ip_address(first)
    last_ip = ipaddress.ip_address(last)
    return [str(network) for network in ipaddress.summarize_address_range(first_ip, last_ip)]


def get_prefix_infos(url: str = IPTOASN_V4_URL, timeout: int = 15):
    for row in get_dataset(url, timeout):
        start_ip, end_ip, asn, country, *description_parts = row
        country = None if country in {"", "None"} else country
        description = "\t".join(description_parts)

        for prefix in range_to_cidrs(start_ip, end_ip):
            yield PrefixInfo(
                prefix=prefix,
                asn=int(asn),
                country=country,
                description=description,
            )
