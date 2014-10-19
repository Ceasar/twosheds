.PHONY: docs test

MODULE = twosheds

init:
	pip install -r requirements.txt

test:
	tox -e py27

coverage:
	py.test --verbose --cov-report term-missing --cov=$(MODULE) tests

interact:
	./scripts/twosheds

install:
	python setup.py install -f

publish:
	python setup.py sdist upload
	python setup.py bdist_wheel upload

docs-init:
	pip install -r docs/requirements.txt

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

clean:
	- rm -r *.egg-info
	- rm -r build
	- rm -r dist
	- rm -r .tox
