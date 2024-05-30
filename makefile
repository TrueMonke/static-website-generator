VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

.PHONY: all
all: venv install run start-server

$(VENV_DIR):
	python3 -m venv $(VENV_DIR)

install: $(VENV_DIR)
	$(PIP) install -r requirements.txt

test: install
	$(PYTHON) -m unittest discover -s src/tests

run: $(VENV_DIR)
	$(PYTHON) -m src.main

start-server:
	$(PYTHON) server.py --dir public

lint:
	set -x
	ruff check --fix
	black src

.PHONY: clean
clean:
	rm -rf $(VENV_DIR)