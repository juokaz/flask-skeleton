# Boilerplate/Skeleton flask application with frontend, admin and api backends

## Running the frontend backend

    source website/venv/bin/activate
    ./manage.py

## Running the admin backend

    source website/venv/bin/activate
    ./manage.py admin

## Running the api backend

    source website/venv/bin/activate
    ./manage.py api

## DB versioning

To generate a new database version

    alembic revision --autogenerate -m "Initial setup"

Upgrade the database to the latest version

    alembic upgrade head

