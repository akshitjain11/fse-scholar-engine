VENV_PATH := $(abspath .venv)
PYTHON := $(VENV_PATH)/bin/python
PIP := $(VENV_PATH)/bin/pip

.PHONY: extract-faculty

.venv: requirements.txt
	python3 -m venv $@
	$(PIP) install --upgrade pip setuptools
	$(PIP) install -r requirements.txt

extract-faculty: .venv
	$(PYTHON) extractor.py	

asu_authors_papers.csv: .venv main.py
	$(PYTHON) main.py

non_affiliate.csv: .venv non_affiliate_extractor.py asu_authors_papers.csv extract-faculty
	$(PYTHON) non_affiliate_extractor.py