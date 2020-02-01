clean:
	rm -rf build/
	rm -rf dist/
	rm -rf docs/.venv docs/build docs/changelog.md
	rm -rf f-lib.egg-info/
	rm -rf tmp/

build: clean
	@python setup.py sdist bdist_wheel

lint: lint-mypy lint-flake8 lint-pylint

lint-flake8:
	@echo "Running flake8..."
	@find f_lib -name '*.py' | xargs pipenv run flake8
	@echo ""

lint-isort:
	@echo "Running isort... If this fails, run 'make sort' to resolve."
	@pipenv run isort . --recursive --check-only
	@echo ""

lint-mypy:
	@echo "Running mypy..."
	@find f_lib -name '*.py' -exec pipenv run mypy {} +
	@echo ""

lint-pylint:
	@echo "Running pylint..."
	@find f_lib -name '*.py' | xargs pipenv run pylint --rcfile=setup.cfg
	@echo ""

sort:
	@pipenv run isort . --recursive --atomic

sync:
	PIPENV_VENV_IN_PROJECT=1 pipenv sync --dev
