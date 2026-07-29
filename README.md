# LPM Toolkit

Local IP-to-ASN lookup API built around a prefix tree.

The idea is simple: there are many public APIs that can tell you information about
one IP address. That is fine for occasional manual checks. It is not fine when you
need streaming or batch processing for thousands or millions of IPs: every request
adds network latency, external dependency risk, and rate-limit pressure.

This service downloads the public `iptoasn` TSV dataset, converts IP ranges into
CIDR prefixes, loads them into a local PyTricia prefix tree, and answers lookups
from local memory.

For IPv4 lookups this is effectively a tiny local database optimized for longest
prefix match:

```text
iptoasn TSV -> IP ranges -> CIDR prefixes -> PyTricia tree -> lookup(ip)
```

The API returns the matched prefix, ASN, country, and description.

## Demo

Swagger UI exposes the protected lookup endpoint:

![Swagger UI](docs/demo/swagger.png)

Lookup response example:

![Lookup demo](docs/demo/lookup.png)

## Run

The project is Docker-first.

Build the image:

```bash
make build
```

Run the API:

```bash
API_TOKEN=my-secret-token make up
```

On first start the app downloads the dataset into:

```text
data/ip2asn-v4.tsv.gz
```

The `data/` directory is mounted into the container, so the dataset is reused on
the next run.

Stop the API:

```bash
make down
```

Tail logs:

```bash
make logs
```

## Lookup

The API requires a Bearer token:

```bash
curl -H 'Authorization: Bearer my-secret-token' \
  http://127.0.0.1:8000/api/v1/lookup/8.8.8.8
```

Example response:

```json
{
  "prefix": "8.8.8.0/24",
  "asn": 15169,
  "country": "US",
  "description": "GOOGLE"
}
```

Another example from the iptoasn dataset:

```bash
curl -H 'Authorization: Bearer my-secret-token' \
  http://127.0.0.1:8000/api/v1/lookup/185.10.149.1
```

```json
{
  "prefix": "185.10.148.0/22",
  "asn": 197558,
  "country": "DE",
  "description": "MUTH"
}
```

Without a token, or with a wrong token, the API returns `401 Unauthorized`.

## Commands

```bash
make build     # build Docker image
make up        # run API, requires API_TOKEN=...
make down      # stop API
make logs      # follow container logs
make lint      # run Ruff checks in Docker
make format    # format code with Ruff in Docker
make fix       # run Ruff autofixes in Docker
make test      # run tests in Docker
make smoke     # build tree and run one lookup in Docker
make check     # run lint and tests in Docker
make hooks     # install pre-commit git hook
make precommit # run pre-commit hooks for all files
```

`pre-commit` itself is installed on the host, but the configured hooks run Ruff
inside Docker Compose:

```bash
python -m pip install pre-commit
make hooks
```

## How It Works

The source dataset has rows like this:

```text
185.10.146.0    185.10.147.255    0         None    Not routed
185.10.148.0    185.10.151.255    197558    DE      MUTH
```

Those ranges are converted into CIDR prefixes:

```text
185.10.148.0 - 185.10.151.255 -> 185.10.148.0/22
```

Each prefix is inserted into a PyTricia tree:

```text
key   = "185.10.148.0/22"
value = PrefixInfo(prefix="185.10.148.0/22", asn=197558, country="DE", description="MUTH")
```

At request time, the API performs longest prefix match locally:

```text
185.10.149.1 -> 185.10.148.0/22 -> ASN 197558, DE, MUTH
```

No external API call is made per lookup.

## Project Layout

```text
app/
  main.py          FastAPI app setup
  dataset.py       download/read iptoasn TSV and convert ranges to CIDRs
  domain.py        domain models
  repository.py    prefix repository interface and PyTricia implementation
  api/v1/          API routes and auth dependency
tests/             pipeline and auth tests
```
