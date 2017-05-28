# How-To-Use Options

1. Wherever you run your playbooks, place `callback_plugins/activity_capture.py` at the root of this directory.

OR 

2. Wherever you keep your other callback plugins, place `activity_capture.py` in that directory. 

### Additional Setup

#### Generating the API token

1. Run the web service in local Docker environment.
2. Run `docker-compose run --rm web python manage.py makesuperuser` to make an admin user.
3. Navigate to the HTTP endpoint's admin (e.g. `http://192.168.99.100:8000/admin`)
4. Make a new user and generate a token for that user.

#### Set the environment variables

`LOG_SERVER_URL` - location of the logging service. (e.g. `http://192.168.99.100:8000/`)
`LOG_SERVER_TOKEN` - API token generated from the logging service's admin.

