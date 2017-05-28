ansible-logging-service
================

A proof of concept RESTful API for logging Ansible activity.


Local development
=================

1. Have `docker-machine` and `docker-compose` installed.
2. Run `docker-compose build` to build the web application container.
3. Run `docker-compose run --rm web python manage.py migrate` to ensure db models are up-to-date.
4. Run `docker-compose up` to start the local development server.

