#!/bin/bash
coverage:
	@coverage run --source='.' manage.py test . && coverage report

run:
	@python manage.py runserver

shell:
	@python manage.py shell_plus --ipython

tests:
	python manage.py test
