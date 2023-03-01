.PHONY: install run integ-test

default: run

install:
	pip install -r requirements.txt

run:
	PYTHONPATH=. python ./app/main.py

integ-test:
	pytest test/integration_tests.py
