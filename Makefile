#!/bin/bash

run:
	@python manage.py runserver

shell:
	@python manage.py shell_plus --ipython

tests:
	python manage.py test
