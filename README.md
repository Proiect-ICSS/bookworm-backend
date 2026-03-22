# bookworm-backend

## Description
This is the backend for the bookworm project.

## Installation
To set up the project, create a python virtual environment using the provided project requirements in **[requirements.txt](requirements.txt)**.

To apply the existing migrations and create the database, please run `python manage.py migrate`. This should create an empty SQLite database with the schema described by the migrations.

## Usage
>Before running the development server, make sure to add a superuser account by using `python manage.py createsuperuser`

To run the backend Django server, run the ***manage.py*** python script with the **runserver** argument (`python manage.py runserver`).

## Project status
***WIP***