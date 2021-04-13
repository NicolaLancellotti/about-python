PYTHON=venv/bin/python3

# ____________________________________________________________________________________________________
# All

.PHONY: all
all:	create-venv \
		format \
		lint \
		test \
		run

# ____________________________________________________________________________________________________
# Help

.PHONY: help
help:
	@echo "Targets:"
	@sed -nr 's/^.PHONY:(.*)/\1/p' ${MAKEFILE_LIST}		

# ____________________________________________________________________________________________________
# Python Virtual Environment

.PHONY: create-venv
create-venv:
	@python3 -m venv venv
	@${PYTHON} -m pip install --upgrade pip
	@${PYTHON} -m pip install -r requirements.txt

# ____________________________________________________________________________________________________
# Format

.PHONY: format
format:
	@${PYTHON} -m black about_python tests
	@${PYTHON} -m isort about_python tests --profile black

# ____________________________________________________________________________________________________
# Lint

.PHONY: lint
lint:
	@${PYTHON} -m pyright --pythonpath=${PYTHON}

# ____________________________________________________________________________________________________
# Test

.PHONY: test
test:
	@${PYTHON} -m pytest tests

# ____________________________________________________________________________________________________
# Run

.PHONY: run
run:
	@${PYTHON} -m about_python
