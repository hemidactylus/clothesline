ROOT_DIR 	:= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# General

tidy: lint-python format-python

test: test-python

docs: make-sphinx-doc

# Specific targets

# (assumes in dev virtualenv)
lint-python:
	flake8 src tests --ignore=PLR0903,PLR1705

# (assumes in dev virtualenv)
format-python:
	black src tests

# (assumes in dev virtualenv)
test-python:
	pytest

# (assumes in dev virtualenv)
make-sphinx-doc:
	cd ${ROOT_DIR}/docs ; make html
