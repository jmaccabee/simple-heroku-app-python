local_shell:
	@export $$(cat .env | xargs); python manage.py shell


migrate:
	@export $$(cat .env | xargs); python manage.py migrate
