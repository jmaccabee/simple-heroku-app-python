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
> heroku config:set SECRET_KEY='<some-secret-key>'

*And you'll need to point Heroku to your production settings file*
> heroku config:set DJANGO_SETTINGS_MODULE=simple_heroku_app.settings.production
