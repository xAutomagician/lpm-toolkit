import csv
import gzip
import ipaddress
from collections.abc import Iterator
from pathlib import Path
from typing import TextIO

import requests

from app.domain import PrefixInfo, PrefixRange

IPTOASN_V4_URL = "https://iptoasn.com/data/ip2asn-v4.tsv.gz"


def download_dataset(
    dest_path: Path,
    url: str = IPTOASN_V4_URL,
    timeout: float = 30.0,
) -> Path:
    resp = requests.get(url, timeout=timeout, stream=True)
    resp.raise_for_status()

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with dest_path.open("wb") as file:
        for chunk in resp.iter_content(chunk_size=1 << 16):
            file.write(chunk)

    return dest_path


def ensure_dataset(
    dest_path: Path,
    url: str = IPTOASN_V4_URL,
    timeout: float = 30.0,
) -> Path:
    if dest_path.exists():
        return dest_path

    return download_dataset(dest_path=dest_path, url=url, timeout=timeout)


def range_to_cidrs(start: str, end: str) -> list[str]:
    start_ip = ipaddress.ip_address(start)
    end_ip = ipaddress.ip_address(end)

    if start_ip.version != end_ip.version:
        raise ValueError("IP range boundaries must use the same IP version")
    if int(start_ip) > int(end_ip):
        raise ValueError("IP range start must be less than or equal to end")

    return [str(network) for network in ipaddress.summarize_address_range(start_ip, end_ip)]


def load_prefix_infos(path: Path) -> Iterator[PrefixInfo]:
    for row in load_prefix_ranges(path):
        for prefix in range_to_cidrs(row.start_ip, row.end_ip):
            yield PrefixInfo(
                prefix=prefix,
                asn=row.asn,
                country=row.country,
                description=row.description,
            )


def load_prefix_ranges(path: Path) -> Iterator[PrefixRange]:
    with _open_text(path) as file:
        reader = csv.reader(file, delimiter="\t")
        for line_number, row in enumerate(reader, start=1):
            if not row:
                continue
            yield _parse_tsv_row(row, line_number)


def _parse_tsv_row(row: list[str], line_number: int) -> PrefixRange:
    if len(row) < 5:
        raise ValueError(f"Invalid TSV row at line {line_number}: expected 5 columns")

    start_ip, end_ip, asn, country, *description_parts = row
    country = None if country in {"", "None"} else country

    return PrefixRange(
        start_ip=start_ip,
        end_ip=end_ip,
        asn=int(asn),
        country=country,
        description="\t".join(description_parts),
    )


def _open_text(path: Path) -> TextIO:
    if path.suffix == ".gz":
        return gzip.open(path, mode="rt", encoding="utf-8", newline="")
    return path.open(mode="r", encoding="utf-8", newline="")
