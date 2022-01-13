from main import db
from main.libs import generate_hashed_password, generate_token
from main.models.category import Category
from main.models.item import Item
from main.models.user import User


def initialize_user_records():
    users = [
        {"email": "dat@gmail.com", "password": "Dat123456"},
        {"email": "dat1@gmail.com", "password": "Dat1234"},
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


def initialize_category_records():
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


def generate_authorization_header(user_id):
    return f"Bearer+ {generate_token(user_id)}"
