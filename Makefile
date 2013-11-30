
init:
	pip install -r requirements.txt

test:
	py.test

install:
	python setup.py install -f

publish:
	python setup.py sdist upload
	python setup.py bdist_wheel upload
