SRC = src/

FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

install:
		uv venv --python 3.10
		uv add --dev flake8 mypy

run:
		uv sync
		uv run python3 -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calls.json

debug:
		uv sync
		uv run python3 -m pdb src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calls.json

clean:
		find . -type d -name "__pycache__" -exec rm -rf {} +
		find . -type d -name ".mypy_cache" -exec rm -rf {} +
		find . -type d -name ".ruff_cache" -exec rm -rf {} +
		find . -name "*.pyc" -delete

fclean: clean
		rm -rf .venv
		rm -f uv.lock
		rm -f maze.txt

lint:
		@clear
		@status=0; \
		uv run flake8 $(SRC) || status=$$?; \
		uv run mypy $(SRC) $(FLAGS) || status=$$?; \
		exit $$status

lint-strict:
		@clear
		@status=0; \
		uv run flake8 $(SRC) || status=$$?; \
		uv run mypy $(SRC) $(FLAGS) --strict || status=$$?; \
		exit $$status

help:
		python3 -m src --help

.PHONY: install run debug clean fclean lint lint-strict help
