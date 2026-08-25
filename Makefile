NAME = main.py
UV = uv
VENV = .venv
PYTHON = $(VENV)/bin/python

all: install

install:
	$(UV) sync

run: install
	$(PYTHON) $(NAME)

debug: install
	$(PYTHON) -m pdb $(NAME)

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint: install
	$(PYTHON) -m flake8 . --exclude=.venv
	$(PYTHON) -m mypy . --exclude '^\.venv/' \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict: install
	$(PYTHON) -m flake8 . --exclude=.venv
	$(PYTHON) -m mypy . --exclude '^\.venv/' --strict

help:
	@echo "to complete"

.PHONY: all install run debug clean lint lint-strict
