import pytest

from main.libs import generate_token
from main.models.category import Category


def test_create_category_successfully(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    new_category = {"name": "item1"}
    response = client.post(
        "/categories",
        json=new_category,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 200
    assert Category.query.filter_by(name=new_category["name"]).one_or_none() is not None


@pytest.mark.parametrize(
    "category",
    [
        {"name": ""},
        {"name": "Dat诶"},
        {},
    ],
)
def test_create_category_with_invalid_data(client, category, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    response = client.post(
        "/categories",
        json=category,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 400
    assert (
        Category.query.filter_by(
            name=category["name"] if "name" in category else None
        ).one_or_none()
        is None
    )


def test_create_category_with_existed_name(client, initialize_records):
    test_db = initialize_records
    exist_category = {"name": "category1"}  # this category is existed in test_db
    user_id = test_db["users"][0].id
    response = client.post(
        "/categories",
        json=exist_category,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 400
    assert Category.query.filter_by(name=exist_category["name"]).one() is not None
    # error will be raised when there are 2 duplicated category names
