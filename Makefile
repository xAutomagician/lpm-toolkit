DOCKER_COMPOSE ?= docker compose

.PHONY: help build up down logs test smoke require-token

help:
	@printf "make build  Build Docker image\n"
	@printf "make up     Run API with Docker Compose; requires API_TOKEN=...\n"
	@printf "make down   Stop Docker Compose stack\n"
	@printf "make logs   Tail API logs\n"
	@printf "make test   Run tests in Docker\n"
	@printf "make smoke  Build tree and run one lookup in Docker\n"

require-token:
	@test -n "$(API_TOKEN)" || (printf "Set API_TOKEN=... before running this target\n"; exit 1)

build:
	$(DOCKER_COMPOSE) build

up: require-token
	API_TOKEN=$(API_TOKEN) $(DOCKER_COMPOSE) up

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f api

test:
	API_TOKEN=test-token $(DOCKER_COMPOSE) run --rm api python -m pytest -q -p no:cacheprovider

smoke:
	API_TOKEN=test-token $(DOCKER_COMPOSE) run --rm api python -B -c "from app.repository import build_prefix_repository; repo = build_prefix_repository(); print(repo.get('8.8.8.8').to_dict())"
