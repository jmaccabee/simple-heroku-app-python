# simple-heroku-app-python
A simple template to bootstrap a new Django project running on Heroku


## Setup instructions
#### Dependencies
Using Mac OS X (10.15.3):

Initially, I ran into an issue where C couldn't compile psycopg2 (a dependency for django-heroku). To resolve the issue I ran the following commands:
> xcode-select --install

> env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2

At that point, I could install the necessary Python requirements.

You'll also need to install the Heroku CLI:
> brew install heroku/brew/heroku


## Heroku config settings
A few Heroku environment variables must be set to run this app:

*You shouldn't expose your secret key*
> heroku config:set SECRET_KEY='some-secret-key'

*And you'll need to point Heroku to your production settings file*
> heroku config:set DJANGO_SETTINGS_MODULE=simple_heroku_app.settings.production

**Optional settings**

You can also point your local directory at your heroku app by running the following:

> git remote add heroku git@heroku.com:your-project-name.git

This will eliminate the need to include the app name in git commands.


## Development
1) Create the database

2) Install the pre-commit hooks:

> pre-commit install

You're ready to go!

3) Create an admin superuser

> python manage.py createsuperuser
