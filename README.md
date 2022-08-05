# Countries data app

App for loading data into postgresql database tables following specific data processing rules. It is a Django-based web application which uses pandas to read data file formats output from extern systems and psycopg2 as adapter to make inserts into database.

## Installation 🔧

Clone the repository in your work folder.

## Configuration

### Create a virtual environment
```
python -m venv .venv
```
### Activate virtual environment

#### Windows
```
.venv\Scripts\activate
```
#### Linux
```
source .venv/bin/activate
```
### Download all packages required
```
pip install -r requirements.txt
```
### Create an environment file

You must create a .env file for project configuration. It must contain following variables:

```
##########################################
# Postgresql database connection settings
##########################################

host=hostname
database=database_name
user=database_user_name
password=database_password
port=postgres_service_port

```

## Run app on test environment
```
python manage.py runserver
```