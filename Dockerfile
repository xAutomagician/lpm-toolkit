FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1
ENV PATH="/opt/venv/bin:${PATH}"

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv

COPY requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.12-slim

ENV PATH="/opt/venv/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV IPTOASN_DATASET_PATH=/app/data/ip2asn-v4.tsv.gz

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY app ./app
COPY pytest.ini .
COPY tests ./tests

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
