PYTHON=python

dist: clean
	${PYTHON} setup.py bdist_wheel

clean:
	rm -rf dist build database_artifact_factory.egg-info

pypi: dist
	${PYTHON} -m twine upload dist/*
