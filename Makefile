SRC = src/

FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint lint-strict visu

install:
	chmod +x install_env.sh
	bash install_env.sh

run:
	@clear
	export HF_HOME="/goinfre/$(USER)/hf-cache" && \
	export TRANSFORMERS_CACHE="/goinfre/$(USER)/hf-cache" && \
	export UV_CACHE_DIR="/goinfre/$(USER)/uv-cache" && \
	uv run python -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calls.json

visu:
	@clear
	export HF_HOME="/goinfre/$(USER)/hf-cache" && \
	export TRANSFORMERS_CACHE="/goinfre/$(USER)/hf-cache" && \
	export UV_CACHE_DIR="/goinfre/$(USER)/uv-cache" && \
	uv run python -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calls.json --visualizer

debug:
	export HF_HOME="/goinfre/$(USER)/hf-cache" && \
	export TRANSFORMERS_CACHE="/goinfre/$(USER)/hf-cache" && \
	uv run python -m pdb -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calls.json

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete

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
