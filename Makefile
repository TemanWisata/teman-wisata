clean:
	uv run cleanpy .

setup-dev:
	uv sync
	uv run pre-commit install

setup:
	uv sync --no-dev

lint:
	uv run ruff check .
	uv run mypy .


setup-ui:
	echo "Setting up the project..."

run:
	uv run main.py
