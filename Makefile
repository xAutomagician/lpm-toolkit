DOCKER_COMPOSE ?= docker compose

.PHONY: help build up down logs test smoke

help:
	@printf "make build  Build Docker image\n"
	@printf "make up     Run API with Docker Compose\n"
	@printf "make down   Stop Docker Compose stack\n"
	@printf "make logs   Tail API logs\n"
	@printf "make test   Run tests in Docker\n"
	@printf "make smoke  Build tree and run one lookup in Docker\n"

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f api

test:
	$(DOCKER_COMPOSE) run --rm api python -m pytest -q -p no:cacheprovider

smoke:
	$(DOCKER_COMPOSE) run --rm api python -B -c "from app.repository import build_prefix_repository; repo = build_prefix_repository(); print(repo.get('8.8.8.8').to_dict())"
