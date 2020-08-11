# Weather API

An API to get min, max, average and median temperature and humidity for given
city and period of time.

## Requirements

- Python3

## Installation

Clone this repo and execute the bootstrap script to get started:

    $ SECRET_KEY=<insert secret key> bin/bootstrap.sh

This will run through the following steps:

1. Create a Python virtual environment
2. Activate the newly created virtual environment
3. Install requirements from requirements.txt
4. Create and run migrations
5. Load fixtures from core/fixtures/cities.json (this may take a while)

## Development

Execute this command to run the Django development server:

    $ SECRET_KEY=<insert secret key> python3 manage.py runserver

Go to http://localhost:8000
