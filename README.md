# Got It's Final Project 

## Requirements

- Python 3.7+
- MySQL 5.7+

## Installation

### Set up virtual environment

```shell
pip install virtualenv
virtualenv venv
source ./venv/bin/activate
```

### Install dependencies

```shell
pip install -r requirements-dev.txt
```

### Setup database
Create 2 different databases: development and test.

Set development database URL in config/base and test database URL in config/test in the following structure:
```
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{passowrd}@localhost:3306/{database_name}"
```

At the first running time, create tables by running the the following commands:
```
python create_table.py
```

## Running

Inside the virtual environment, run:

```shell
python run.py
```
## Testing

For testing, run the following command:
```
ENVIRONMENT=test pytest
```
If test database tables has not set, run the following command to initialize ones:
```
flask db upgrade
```
If test tables are already existed and conflict with current models, remove all files inside migrations/versions folder and all tables inside test database.

Create a revision file in migrations/version by running:
```
flask db migrate
```
Then do the initialization step as above.

