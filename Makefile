.PHONY: all help pip-install pip-install-dev

help: ## Display this help message
	@echo "Please use \`make <target>\` where <target> is one of"
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | grep -v -e '^[^[:alnum:]]' -e '^$@$$'


all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

pip-install:
	pip install --upgrade pip pip-tools
	pip-sync requirements.txt

pip-install-dev:
	pip install --upgrade pip pip-tools
	pip-sync requirements.txt requirements-dev.txt


pip-update:
	pip install --upgrade pip pip-tools
	# pip-compile requirements.in
	# pip-compile requirements-dev.in
	pip-sync requirements.txt requirements-dev.txt

run:
	python manage.py runserver

migration:
	python manage.py makemigrations

migrate:
	python manage.py migrate

superuser:
	python manage.py createsuperuser

checkmigrations:
	python manage.py makemigrations --check --no-input --dry-run

server:
	python manage.py migrate && python manage.py runserver

# linters
lint:
	flake8 palyanytsya
	mypy palyanytsya

black:
	python -m black palyanytsya

cleanimports:
	isort .
	autoflake -r -i --remove-all-unused-imports --ignore-init-module-imports project_name

clean-lint: cleanimports black lint
