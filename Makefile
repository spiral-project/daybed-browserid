VIRTUALENV=virtualenv
VENV := $(shell echo $${VIRTUAL_ENV-.venv})
PYTHON=$(VENV)/bin/python
DEV_STAMP=$(VENV)/.dev_env_installed.stamp
INSTALL_STAMP=$(VENV)/.install.stamp
SPHINX_BUILD = sphinx-build

.IGNORE: clean
.PHONY: all docs install virtualenv tests

OBJECTS = .venv .coverage

all: install
install: $(INSTALL_STAMP)
$(INSTALL_STAMP): $(PYTHON)
	$(PYTHON) setup.py develop
	$(VENV)/bin/pip install git+https://github.com/spiral-project/daybed.git#9c84dd70
	touch $(INSTALL_STAMP)

virtualenv: $(PYTHON)
$(PYTHON):
	virtualenv $(VENV)

clean:
	rm -fr $(OBJECTS) $(DEV_STAMP) $(INSTALL_STAMP)
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

serve: install install-dev
	$(VENV)/bin/pserve conf/development.ini --reload
