.PHONY: install dev test lint format check clean docker-build docker-up docker-down

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/unit -v

test-integration:
	pytest tests/integration -v

lint:
	ruff check src tests

format:
	ruff format src tests

check: lint test

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache reports_output/*

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

