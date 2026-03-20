PYTHON ?= python3

.PHONY: help install install-dev test build clean version

help:
	@echo "Available targets:"
	@echo "  install      Install package"
	@echo "  install-dev  Install package with dev dependencies"
	@echo "  test         Run pytest"
	@echo "  build        Build wheel and sdist"
	@echo "  version      Print CLI version"
	@echo "  clean        Remove build artifacts"

install:
	$(PYTHON) -m pip install -e .

install-dev:
	$(PYTHON) -m pip install -e '.[dev]'

test:
	$(PYTHON) -m pytest tests/ -q

build:
	$(PYTHON) -m build

version:
	$(PYTHON) -m goskill.cli --version

clean:
	rm -rf build dist *.egg-info .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
