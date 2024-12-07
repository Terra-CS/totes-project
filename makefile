#Make file
PROJECT_NAME = de-totes-project
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}/src
SHELL := /bin/bash
PROFILE = default
PIP:=pip

## Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

#Activate venv 
ACTIVATE_ENV := source venv/bin/activate

define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

## Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install pip-tools)
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

##install bandit

bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Install safety
safety:
	$(call execute_in_env, $(PIP) install safety)

## Install black
black:
	$(call execute_in_env, $(PIP) install black)

## Install flake8
flake8:
	$(call execute_in_env, $(PIP) install flake8)

## Set up dev requirements (bandit, safety, black)
dev-setup: bandit safety black flake8

security-test:
	$(call execute_in_env, safety check -r ./requirements.txt)
	$(call execute_in_env, bandit -lll --skip B101 -v -r src/ test/)

## Run the black code check
run-black:
	$(call execute_in_env, black src test)

## Run flake8 check
run-flake8:
	$(call execute_in_env, flake8 src/* test/*)

## Run the unit tests
unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest -v test/*)

## Run all checks
run-checks: security-test run-flake8 unit-test




