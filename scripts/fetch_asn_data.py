from pathlib import Path

import requests


IPTOASN_V4_URL = "https://iptoasn.com/data/ip2asn-v4.tsv.gz"


def download_ipv4_dataset(dest_path: Path, url: str = IPTOASN_V4_URL, timeout: float = 30.0) -> Path:
    """
    Fetch the gzip TSV dataset to `dest_path`. Requires network access.
    Lives here, not in the repository module — this is a one-shot CLI
    concern, not something the running API ever calls.
    """
    resp = requests.get(url, timeout=timeout, stream=True)
    resp.raise_for_status()
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1 << 16):
            f.write(chunk)
    return dest_path
