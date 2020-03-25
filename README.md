# simple-heroku-app-python
A simple template to bootstrap a new Heroku project


## Setup instructions
Using Mac OS X:

Initially, I ran into an issue where C couldn't compile psycopg2 (a dependency for django-heroku). To resolve the issue I ran the following commands:
> xcode-select --install
> env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2

At that point, I could install the necessary requirements.
