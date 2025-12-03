VENV_PATH := $(abspath .venv)
PYTHON := $(VENV_PATH)/bin/python
PIP := $(VENV_PATH)/bin/pip

.PHONY: extract-faculty

.venv:
	python3 -m venv $@
	$(PIP) install --upgrade pip setuptools
	$(PIP) install -r requirements.txt

extract-faculty: .venv
	$(PYTHON) extractor.py	
