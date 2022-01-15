export PIPENV_VERBOSITY=-1

develop:
	bin/setup.dev -y

clean:
	find . -name '*.pyc' -delete

docker_clean_build:
	bin/dc build --no-cache runserver

fixture_products:
	bin/djmanage dumpdata --natural-primary --natural-foreign --format json --indent 2 products > fixtures/demo/products.json

loaddemo:
	bin/djmanage loaddata fixtures/demo/products.json

pullstaging:
	bin/djmanage pull_staging_data

test:
	bin/test

fix-file-ownership:
	bin/fix-file-ownership

mypy:
	pipenv run mypy

isort:
	pipenv run isort fanout

flake8:
	pipenv run flake8

test_in_docker:
	bin/djtest

format:
	pipenv run black fanout wsgi.py manage.py

lint:
	pipenv run black --check fanout wsgi.py manage.py

autoflake:
	autoflake -r -i --expand-star-imports --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables --ignore-init-module-imports fanout/apps/
