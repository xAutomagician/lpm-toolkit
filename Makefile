DOCKER_COMPOSE ?= docker compose

.PHONY: help build up down logs lint format fix test smoke check hooks precommit require-token

help:
	@printf "make build      Build Docker image\n"
	@printf "make up         Run API with Docker Compose; requires API_TOKEN=...\n"
	@printf "make down       Stop Docker Compose stack\n"
	@printf "make logs       Tail API logs\n"
	@printf "make lint       Run Ruff checks in Docker\n"
	@printf "make format     Format code with Ruff in Docker\n"
	@printf "make fix        Run Ruff autofixes in Docker\n"
	@printf "make test       Run tests in Docker\n"
	@printf "make smoke      Build tree and run one lookup in Docker\n"
	@printf "make check      Run lint and tests in Docker\n"
	@printf "make hooks      Install pre-commit git hook\n"
	@printf "make precommit  Run pre-commit hooks for all files\n"

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

lint:
	API_TOKEN=test-token $(DOCKER_COMPOSE) run --rm api ruff check .

format:
	API_TOKEN=test-token $(DOCKER_COMPOSE) run --rm api ruff format .

fix:
	API_TOKEN=test-token $(DOCKER_COMPOSE) run --rm api ruff check --fix .

test:
	API_TOKEN=test-token $(DOCKER_COMPOSE) run --rm api python -m pytest -q -p no:cacheprovider

smoke:
	API_TOKEN=test-token $(DOCKER_COMPOSE) run --rm api python -B -c "from app.repository import build_prefix_repository; repo = build_prefix_repository(); print(repo.get('8.8.8.8').to_dict())"

check: lint test

hooks:
	pre-commit install

precommit:
	pre-commit run --all-files
