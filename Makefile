.PHONY: sync rank status validate test lint format check

sync:
	uv run oplab sync --revision main --allow-network

rank:
	uv run oplab rank

status:
	uv run oplab status

validate:
	uv run oplab validate

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run mypy src

format:
	uv run ruff format .

check: lint test
