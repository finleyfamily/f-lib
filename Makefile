CI := $(if $(CI),yes,no)
SHELL := /bin/bash

ifeq ($(CI), yes)
	POETRY_OPTS = "-v"
	PRE_COMMIT_OPTS = --show-diff-on-failure --verbose
endif

help: ## show this message
	@awk \
		'BEGIN {FS = ":.*##"; printf "\nUsage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' \
		$(MAKEFILE_LIST)

build: ## build the PyPi release
	@poetry build

.PHONY: docs
docs: ## delete build artifacts, start sphinx-autobuild server, & open browser window
	@if [[ -z "$${CI}" ]]; then \
		$(MAKE) --no-print-directory -C docs docs; \
	else \
		$(MAKE) --no-print-directory docs-changes; \
	fi

docs-changes: ## build HTML docs; only builds changes detected by Sphinx
	@$(MAKE) --no-print-directory -C docs html

docs-clean: ## delete build artifacts & build HTML docs
	@$(MAKE) --no-print-directory -C docs clean html

docs-linkcheck: ## check external links
	@$(MAKE) --no-print-directory -C docs linkcheck

fix: fix-ruff fix-black run-pre-commit ## run all automatic fixes

fix-black: ## automatically fix all black errors
	@poetry run black .

fix-imports: ## automatically fix all import sorting errors
	@poetry run ruff check . --fix-only --fixable I001

fix-ruff: ## automatically fix everything ruff can fix (implies fix-imports)
	@poetry run ruff check . --fix-only

lint: lint-black lint-ruff lint-pyright ## run all linters

lint-black: ## run black
	@echo "Running black... If this fails, run 'make fix-black' to resolve."
	@poetry run black . --check --color --diff
	@echo ""

lint-pyright: ## run pyright
	@echo "Running pyright..."
	@npm exec --no -- pyright --venvpath ./
	@echo ""

lint-ruff: ## run ruff
	@echo "Running ruff... If this fails, run 'make fix-ruff' to resolve some error automatically, other require manual action."
	@poetry run ruff check .
	@echo ""

open-docs: ## open docs (HTML files must already exists)
	@$(MAKE) --no-print-directory -C docs open

run-pre-commit: ## run pre-commit for all files
	@poetry run pre-commit run $(PRE_COMMIT_OPTS) \
		--all-files \
		--color always

setup: setup-poetry setup-pre-commit setup-npm ## setup development environment

setup-npm: ## install node dependencies with npm
	@npm ci

setup-poetry: ## setup python virtual environment
	@if [[ -d .venv ]]; then \
		poetry run python -m pip --version >/dev/null 2>&1 || rm -rf ./.venv/* ./.venv/.*; \
	fi
	@poetry check
	@poetry install $(POETRY_OPTS) --sync

setup-pre-commit: ## install pre-commit git hooks
	@poetry run pre-commit install

spellcheck: ## run cspell
	@echo "Running cSpell to checking spelling..."
	@npm exec --no -- cspell lint . \
		--color \
		--config .vscode/cspell.json \
		--dot \
		--gitignore \
		--must-find-files \
		--no-progress \
		--relative \
		--show-context

test:  ## run integration and unit tests
	@echo "Running integration & unit tests..."
	@poetry run pytest $(PYTEST_REPORT_OPTS) \
		--cov f_lib \
		--cov-report term-missing:skip-covered \
		--dist worksteal \
		--numprocesses logical
