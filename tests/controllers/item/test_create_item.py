import pytest

from main.libs import generate_token
from main.models.item import Item


def test_create_item_successfully(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    new_item = {"name": "item3", "description": "bla blo3"}
    category_id = test_db["categories"][0].id
    response = client.post(
        f"/categories/{category_id}/items",
        json=new_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 200
    assert Item.query.filter_by(name=new_item["name"]).one_or_none() is not None


@pytest.mark.parametrize(
    "item",
    [
        {"name": "test-item1", "description": ""},
        {"name": "", "description": "bla blo"},
        {"name": "", "description": ""},
        {"description": ""},
        {"name": ""},
        {},
    ],
)
def test_create_item_with_invalid_data(client, item, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    category_id = test_db["categories"][0].id
    response = client.post(
        f"/categories/{category_id}/items",
        json=item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 400
    assert (
        Item.query.filter_by(
            name=item["name"] if "name" in item else None
        ).one_or_none()
        is None
    )


def test_create_item_with_existed_name(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    category_id = test_db["categories"][0].id
    new_item = {"name": "item1", "description": "bla blo3"}
    response = client.post(
        f"/categories/{category_id}/items",
        json=new_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 400
    assert Item.query.filter_by(name=new_item["name"]).one() is not None
    # error will be raise if there are 2 duplicated item name


def test_create_item_with_unknown_category_id(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    category_id = 100000  # random category id
    new_item = {"name": "item1", "description": "bla blo3"}
    response = client.post(
        f"/categories/{category_id}/items",
        json=new_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 404
    assert (
        Item.query.filter_by(
            name=new_item["name"], category_id=category_id
        ).one_or_none()
        is None
    )
