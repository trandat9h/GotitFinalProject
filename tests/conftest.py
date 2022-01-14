import os
import sys
from pathlib import Path

import pytest
from alembic.command import upgrade
from alembic.config import Config

from main import app as _app
from main import db
from main.libs import generate_hashed_password
from main.models.category import Category
from main.models.item import Item
from main.models.user import User

if os.getenv("ENVIRONMENT") != "test":
    print('Tests should be run with "ENVIRONMENT=test"')
    sys.exit(1)

ALEMBIC_CONFIG = (
    (Path(__file__) / ".." / ".." / "migrations" / "alembic.ini").resolve().as_posix()
)


@pytest.fixture(scope="session", autouse=True)
def app():
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="session", autouse=True)
def recreate_database(app):
    db.reflect()
    db.drop_all()
    _config = Config(ALEMBIC_CONFIG)
    upgrade(_config, "heads")


@pytest.fixture(scope="function", autouse=True)
def session(monkeypatch):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function", autouse=True)
def client(app, session):
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def initialize_records():
    test_db = {"users": [], "categories": [], "items": [], "page": 1}
    users = [
        {"email": "dat1@gmail.com", "password": "Dat1234"},
        {"email": "dat@gmail.com", "password": "Dat12345"},
    ]
    categories = [
        {"name": "category1"},
        {"name": "category2"},
    ]
    items = [
        {"name": "item1", "description": "bla blo1"},
        {"name": "item2", "description": "bla blo2"},
    ]

    for user in users:
        auth_data = generate_hashed_password(user["password"])
        new_user = User(
            email=user["email"],
            hashed_password=auth_data["hashed_password_with_salt"],
            salt=auth_data["salt"],
        )
        db.session.add(new_user)
        db.session.commit()
        test_db["users"].append(new_user)

    # all test categories belong to first test user
    for category in categories:
        new_category = Category(name=category["name"], user_id=test_db["users"][0].id)
        db.session.add(new_category)
        db.session.commit()
        test_db["categories"].append(new_category)

    # all test items belong to first test category
    for item in items:
        new_item = Item(
            name=item["name"],
            description=item["description"],
            user_id=test_db["users"][0].id,
            category_id=test_db["categories"][0].id,
        )
        db.session.add(new_item)
        db.session.commit()
        test_db["items"].append(new_item)

    return test_db
