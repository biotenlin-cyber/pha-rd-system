.PHONY: up down migrate seed dev-be dev-fe test fmt lint

up:
	docker compose up -d postgres

down:
	docker compose down

migrate:
	cd backend && uv run alembic upgrade head

seed:
	cd backend && uv run python -m scripts.seed --reset

dev-be:
	cd backend && uv run uvicorn app.main:app --reload --port 8000

dev-fe:
	cd frontend && pnpm dev

install-be:
	cd backend && uv sync

install-fe:
	cd frontend && pnpm install

test:
	cd backend && uv run pytest -q

fmt:
	cd backend && uv run ruff format . && uv run ruff check --fix .
	cd frontend && pnpm format

lint:
	cd backend && uv run ruff check .
	cd frontend && pnpm lint && pnpm vue-tsc --noEmit
