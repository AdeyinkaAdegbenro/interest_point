# Project Notes

## Tech Stack

The tech stack is in Python 3, Django, PostgreSQL, JavaScript and AngularJS. Unit Tests are present in `points/tests.py` and `accounts/tests.py`.

## Deployed Application

The deployed application can be found at https://rideco-pointofinterest.herokuapp.com/ 

## Database Diagram

This can be found in the root folder as `RideCo _ Database ER diagram .png`

![db erm diagram](https://i.imgur.com/6qrhYW6.png)

## Installation Instructions

- Once you are in the interestpoint directory, Set up a Python virtual environment and install requirements:

```bash
virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

```

- Database Setup

Run `psql` on terminal to connect to a PostgreSQL database server run the below commands to set up the database according to the app's database settings

```sql
CREATE DATABASE interest_points;

CREATE USER khaliat WITH PASSWORD 'password';

ALTER ROLE khaliat SET client_encoding TO 'utf8';
ALTER ROLE khaliat SET default_transaction_isolation TO 'read committed';
ALTER ROLE khaliat SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE interest_points TO khaliat;

-- To enable creation of test database
ALTER ROLE khaliat CREATEDB;
```

- Run migrations

```bash
python manage.py migrate
```

- Run Unit tests

```bash
python manage.py test
```

- In the working directory, run the below command to start the application

```bash
python manage.py runserver
```

- Then visit the application on http://localhost:8000/ to use it.

### Useful features to add next

Add a feature that helps users to see what points of interests are trending/recommended across the application from other users. This feature would also let them search the whole application for other users' points of interests.

A feature to share a point of interest on social media with friends.
