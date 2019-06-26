# Eurovision REST API with Django & Django Rest Framework
> A simple Web API to allow to view and edit the artists, contests, countries, participants, voters, and votes for Eurovision.

The REST API for Eurovision contests.

![](header.png)

## Installing / Getting started

To clone and run this repository you'll need [Git](https://git-scm.com/downloads) and [Python](https://www.python.org/downloads/) installed on your computer.

First from your terminal:

```bash
git clone https://github.com/isidaruk/eurovision_project.git
cd eurovision_project/
```

Then create and activate a virtual environment for this project. From your terminal:

```bash
# Install and activate venv
$ python3.6 -m venv venv
$ source ./venv/bin/activate

# Install dependencies
$ pip install -U requirements.txt
```

The project is configured to use [Postgres](https://www.postgresql.org/download/) database, so be sure it's installed.
Create a database for this project and put the congfiguration to .env file inside eurovision_project/ folder. 
Example .env:

```
DEBUG=on
SECRET_KEY='test'
# POSTGRES
#
# DATABASE_URL=psql://<username>:<password>@<host>:<port>/<database_name>
DATABASE_URL=psql://test:test@localhost/testdb
```

Then it's time to run migrations. From your terminal:

```bash
# Run DB migrations 
$ python manage.py makemigrations

# Create superuser
$ python manage.py createsuperuser

# Run Server (http://localhst:8000)
python manage.py runserver
```

The API is up and running now.

To populate the db with some data use the management commands in the following order. From your terminal:

```bash
# Populate the db with countries
$ python manage.py loadcountries all_countries.csv

# Add artists
$ python manage.py loadartists artists.csv

# Add contests
$ python manage.py loadcontests new_contests.csv

# Add partisipants
$ python manage.py loadparticipants participants.csv

# Run Server again if you stopped it (http://localhst:8000)
python manage.py runserver
```

## Developing

In order to start developing the project further:

```bash
git clone https://github.com/isidaruk/eurovision_project.git
cd eurovision_project/
```

And follow all steps from the Installing / Getting started section.

## Features and Endpoints

What's all the bells and whistles this Eurovision project can perform?
Here they are:
* Allows CRUD operation on artists, contests, countries, participants, voters, and votes objects
* You can also populate db with csv files for the API
* Web browsable api /api/v0/, and admin /admin/
* You can List all participants, or create a new participant. The same is true for other data.
    * GET     /api/v0/participants/
    * POST    /api/v0/participants/
* Also Retrieve, update or delete a participant instance. The same is true for other data.
    * GET     /api/v0/participants/:id
    * PUT     /api/v0/participants/:id
    * DELETE  /api/v0/participants/:id
* POST Votes are allowed only for a participants with valid token
* Cases for Votes included (not allowed post data for own country, give votes twice, etc.)
* In Admin Participants you can view, sort (by score), and filter participants for specific year or contest
* Try it on your own...

## Configuration

You can alter configurations in pytest.ini and setup.cfg using the project. Where pytest, flake8 and isort are configured.

#### Test

You can write your own tests for the project. Or simply, run existing tests for votes app.

Example:
```bash
pytest votes/tests/test_views.py
```

or with verbose output:
```bash
pytest votes/tests/test_models.py -vv
```

## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

1. Fork it (<https://github.com/isidaruk/eurovision_project/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Links

- Project homepage: -
- Repository: https://github.com/isidaruk/eurovision_project
- Issue tracker: https://github.com/isidaruk/eurovision_project/issues
  - In case of sensitive bugs like security vulnerabilities, please contact
    my@email.com directly instead of using issue tracker. We value your effort
    to improve the security and privacy of this project!

## Licensing

The code in this project is licensed under MIT license.
