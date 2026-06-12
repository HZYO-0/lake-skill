.PHONY: help install test lint format typecheck check package-skill clean intake doctor demo

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in development mode
	pip install -e ".[dev]"

test:  ## Run tests
	pytest -q

lint:  ## Run linter
	ruff check .

format:  ## Format code
	ruff format .

typecheck:  ## Run type checker
	mypy cli

check: lint typecheck test  ## Run all checks

package-skill:  ## Package skill for ChatGPT
	cd skills/lake-skill && zip -r ../../dist/skill.zip . -x "*.pyc" -x "__pycache__/*"

clean:  ## Clean build artifacts
	rm -rf dist/ build/ *.egg-info
	python -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"
	python -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]"

intake:  ## Generate intake card
	lake-skill intake --out .

doctor:  ## Run data readiness check
	lake-skill doctor --messages work/raw_messages.jsonl --out .

demo:  ## Generate demo package
	cd examples && python generate_examples.py
