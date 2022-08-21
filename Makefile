# blog_hillel
# Makefile


.ONESHELL:
PHONY: install-python-requirements install-requirements check-python-requirements check-requirements test makemessages compilemessages check clean runserver migrate makemigrations collectstatic build-error-pages shell dbshell createsuperuser bumpversion setup-env install-pre-commit-hook bootstrap build up down restart ps logs sh check-d test-d makemessages-d compilemessages-d makemigrations-d migrate-d collectstatic-d build-error-pages-d shell-d dbshell-d createsuperuser-d help
NAME ?= blog_hillel
EXTENSIONS ?= py,html,txt,xml,eml
TRASH_DIRS ?= build .mypy_cache .pytest_cache __pycache__ htmlcov
TRASH_FILES ?= .coverage coverage.xml *.pid Pipfile.lock
HOST ?= 0.0.0.0
PORT ?= 8080
ENVIRONMENT ?= dev
SETTINGS ?= $(NAME).settings.$(ENVIRONMENT)
VERSION=`python -c "import configparser; config = configparser.ConfigParser(); config.read('setup.cfg'); print(config['metadata']['version']);"`
MANAGE ?= django-admin
COMPOSE ?= docker-compose
SERVICE ?= blog_hillel-dev
REPOSITORY_NAME ?= blog_hillel

install-python-requirements:
	python -m pip install .[$(ENVIRONMENT)];\


install-requirements: install-python-requirements


check-python-requirements:
	pip-outdated setup.cfg;\


check-requirements: check-python-requirements


test:
	PYTHONPATH="$${PYTHONPATH}:$${PWD}" DJANGO_SETTINGS_MODULE=$(SETTINGS) $(RUN) pytest --import-mode=importlib --cov=blog_hillel$(TESTS);\


makemessages:
	for locale in `ls $(NAME)/locale`; do\
		PYTHONPATH="$${PYTHONPATH}:$${PWD}" DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) makemessages --locale=$${locale} --extension=$(EXTENSIONS) -d django --traceback;\
	done;\


compilemessages:
	PYTHONPATH="$${PYTHONPATH}:$${PWD}" DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) compilemessages;\


check:
	pre-commit run --all-files;\


clean:
	for file in $(TRASH_FILES); do\
		find -iname $${file} -print0 | xargs -0 rm -rf;\
	done;\
	for dir in $(TRASH_DIRS); do\
		find -type d -name $${dir} ! -path "*/.direnv/*" -print0 | xargs -0 rm -rf;\
	done;\


runserver:
	PYTHONPATH="$${PYTHONPATH}:$${PWD}" DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) runserver $(HOST):$(PORT) --traceback;\


migrate:
	PYTHONPATH="$${PYTHONPATH}:$${PWD}" DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) migrate --traceback;\


makemigrations:
	PYTHONPATH="$${PYTHONPATH}:$${PWD}" DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) makemigrations --traceback $(APP);\


collectstatic:
	PYTHONPATH="$${PYTHONPATH}:$${PWD}" DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) collectstatic --traceback --noinput;\


build-error-pages:
	PYTHONPATH="$${PYTHONPATH}:$${PWD}" DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) build --traceback --skip-static --skip-media --keep-build-dir;\


shell:
	PYTHONPATH="$${PYTHONPATH}:$${PWD}" DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) shell --traceback;\


dbshell:
	PYTHONPATH="$${PYTHONPATH}:$${PWD}" DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) dbshell --traceback;\


createsuperuser:
	PYTHONPATH="$${PYTHONPATH}:$${PWD}" DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) createsuperuser --traceback;\


bumpversion:
	git tag -a $(VERSION) -m "v$(VERSION)";\


setup-env:
	cp .env.example .env;\
	direnv allow;\


install-pre-commit-hook:
	pre-commit install;\


bootstrap: setup-env install-python-requirements install-pre-commit-hook


build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 $(COMPOSE) build;\


up:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 $(COMPOSE) up --build -d;\


down:
	$(COMPOSE) down;\


restart: down up


ps:
	$(COMPOSE) ps;\


logs:
	$(COMPOSE) logs -f -t;\


sh:
	$(COMPOSE) exec $(SERVICE) bash;\


check-d:
	$(COMPOSE) exec $(SERVICE) make check;\


test-d:
	$(COMPOSE) exec $(SERVICE) make test;\


makemessages-d:
	$(COMPOSE) exec $(SERVICE) make makemessages;\


compilemessages-d:
	$(COMPOSE) exec $(SERVICE) make compilemessage;\


makemigrations-d:
	$(COMPOSE) exec $(SERVICE) make makemigrations;\


migrate-d:
	$(COMPOSE) exec $(SERVICE) make migrate;\


collectstatic-d:
	$(COMPOSE) exec $(SERVICE) make collectstatic;\


build-error-pages-d:
	$(COMPOSE) exec $(SERVICE) make build-error-pages;\


shell-d:
	$(COMPOSE) exec $(SERVICE) make shell;\


dbshell-d:
	$(COMPOSE) exec $(SERVICE) make dbshell;\


createsuperuser-d:
	$(COMPOSE) exec $(SERVICE) make createsuperuser;\


help:
	@echo "    help:"
	@echo "        Show this help."
	@echo "    [LOCAL DEVELOPMENT]:"
	@echo "        install-python-requirements:"
	@echo "            Install python requirements."
	@echo "        install-requirements:"
	@echo "            Install all requirements."
	@echo "        check-python-requirements:"
	@echo "            Check python outdated requirements."
	@echo "        check-requirements:"
	@echo "            Check all outdated requirements."
	@echo "        test:"
	@echo "            Run tests, can specify tests with 'TESTS' variable."
	@echo "        makemessages:"
	@echo "            Harvest translations."
	@echo "        compilemessages:"
	@echo "            Compile translations."
	@echo "        check:"
	@echo "            Perform some code checks."
	@echo "        clean:"
	@echo "            Recursively delete useless autogenerated files and directories, directories and files lists can be overridden through 'TRASH_DIRS' and 'TRASH_FILES' variables."
	@echo "        runserver:"
	@echo "            Run django development server, by default at all network interfaces and 8080 port."
	@echo "        migrate:"
	@echo "            Apply migrations."
	@echo "        makemigrations:"
	@echo "            Create new migrations for changed models."
	@echo "        collectstatic:"
	@echo "            Collect django third packages static."
	@echo "        build-error-pages:"
	@echo "            Build static error pages."
	@echo "        shell:"
	@echo "            Run django development shell."
	@echo "        dbshell:"
	@echo "            Run database shell."
	@echo "        createsuperuser:"
	@echo "            Create django superuser."
	@echo "        bumpversion:"
	@echo "            Tag current code revision from version file."
	@echo "        setup-env:"
	@echo "            Copy example environment config for development."
	@echo "        install-pre-commit-hook:"
	@echo "            Setup pre commit hook."
	@echo "        bootstrap:"
	@echo "            Bootstrap project."
	@echo "    [DOCKER DEVELOPMENT]:"
	@echo "        build:"
	@echo "            Build docker images."
	@echo "        up:"
	@echo "            Start docker containers."
	@echo "        down:"
	@echo "            Stop docker containers."
	@echo "        restart:"
	@echo "            Restart docker containers."
	@echo "        ps:"
	@echo "            List docker containers."
	@echo "        logs:"
	@echo "            Show docker containers logs. 'SERVICE' arg can be used to show logs only from specific service."
	@echo "        sh:"
	@echo "            Start interactive shell in docker container. 'SERVICE' arg can be used to specify service."
	@echo "        check-d:"
	@echo "            Perform some code checks in docker container. 'SERVICE' arg can be used to specify service."
	@echo "        test-d:"
	@echo "            Run tests, can specify tests in docker container with 'TESTS' variable. 'SERVICE' arg can be used to specify service."
	@echo "        makemessages-d:"
	@echo "            Harvest translations in docker container. 'SERVICE' arg can be used to specify service."
	@echo "        compilemessages-d:"
	@echo "            Compile translations in docker container. 'SERVICE' arg can be used to specify service."
	@echo "        makemigrations-d:"
	@echo "            Create new migrations for changed models in docker container. 'SERVICE' arg can be used to specify service."
	@echo "        migrate-d:"
	@echo "            Apply migrations in docker container. 'SERVICE' arg can be used to specify service."
	@echo "        collectstatic-d:"
	@echo "            Collect django third packages static in docker container. 'SERVICE' arg can be used to specify service."
	@echo "        build-error-pages-d:"
	@echo "            Build static error pages in docker container. 'SERVICE' arg can be used to specify service."
	@echo "        shell-d:"
	@echo "            Run django development shell in docker container. 'SERVICE' arg can be used to specify service."
	@echo "        dbshell-d:"
	@echo "            Run database shell in docker container. 'SERVICE' arg can be used to specify service."
	@echo "        createsuperuser-d:"
