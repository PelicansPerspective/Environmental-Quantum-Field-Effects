# Environmental Quantum Field Effects - Makefile
# Common development and testing commands

.PHONY: help install test lint format clean docs demo

# Default target
help:
	@echo "Environmental Quantum Field Effects - Development Commands"
	@echo "=========================================================="
	@echo ""
	@echo "Available targets:"
	@echo "  install    Install package and dependencies"
	@echo "  test       Run all tests with coverage"
	@echo "  test-fast  Run fast tests only"
	@echo "  lint       Run code linting checks"
	@echo "  format     Auto-format code"
	@echo "  clean      Clean build artifacts"
	@echo "  docs       Build documentation"
	@echo "  demo       Run basic demonstration"
	@echo "  analyze    Run advanced analysis"
	@echo "  validate   Run physics validation"
	@echo ""

# Installation
install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev,docs]"

# Testing
test:
	python -m pytest tests/ -v --cov=simulations --cov-report=html --cov-report=term

test-fast:
	python -m pytest tests/ -v -m "not slow"

test-physics:
	python -m pytest tests/test_physics_validation.py -v

test-integration:
	python -m pytest tests/test_integration.py -v

# Code quality
lint:
	flake8 simulations/ tests/ examples/
	mypy simulations/

format:
	black simulations/ tests/ examples/
	isort simulations/ tests/ examples/

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Documentation
docs:
	cd docs && sphinx-build -b html . _build/html
	@echo "Documentation built in docs/_build/html/"

docs-clean:
	cd docs && rm -rf _build/

# Demonstrations
demo:
	python examples/basic_demo.py

analyze:
	python examples/advanced_analysis.py

# Validation
validate:
	python tests/test_integration.py
	python -c "from tests.test_physics_validation import validate_physics_bounds; print('Physics validation complete')"

# Package building
build:
	python setup.py sdist bdist_wheel

# Release preparation
release-check: test lint
	python setup.py check --strict --metadata
	twine check dist/*

# Development environment setup
dev-setup: install-dev
	pre-commit install
	@echo "Development environment ready!"

# Continuous integration simulation
ci: install test lint
	@echo "CI simulation complete"
