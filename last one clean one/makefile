NAME = src
UV = uv
PYTHON = $(UV) run python

.PHONY: all install run debug clean lint lint-strict

all: install

install:
	$(UV) sync

run: install
	$(PYTHON) -m $(NAME).__main__ $(ARGS)

debug: install
	$(PYTHON) -m pdb -m $(NAME) $(ARGS)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".venv" -exec rm -rf {} +
	find . -type d -name "output" -exec rm -rf {} +

lint:
	flake8 . --exclude=.venv,.git,__pycache__,llm_sdk
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . --exclude=.venv,.git,__pycache__,llm_sdk
	mypy . --strict
