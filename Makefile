SHELL=/bin/bash

help:
	@echo 'Makefile for Quake Log Parser / API                           '
	@echo '                                                              '
	@echo 'Usage:                                                        '
	@echo '    make clean              Remove python compiled files      '
	@echo '    make requirements_dev   Install required packages to Dev  '
	@echo '    make up                 Enable mongo docker container     '
	@echo '    make lint               Verify code lint                  '
	@echo '    make unit               Run unit tests                    '
	@echo '    make migrate_db         Apply the migrations to db        '
	@echo '    make run                Execute script that parse game.log'
	@echo '    make runserver          Run the application               '
	@echo '                                                              '

clean:
	find . -iname '*.pyc' -delete;
	find . -iname '*.pyo' -delete;
	find . -iname '__pycache__' -delete;
	rm -rf .pytest_cache;
	rm -rf .cache;

requirements_dev:
	pip install -r requirements/requirements_dev.txt

up:
	docker-compose up -d

unit:clean
	python -m pytest --show-capture=no

lint:
	isort --check
	flake8

migrate_db:
	python manage.py migrate
	python manage.py makemigrations

run:
	python run.py

runserver:
	python manage.py runserver

