import pytest

from main.libs import generate_token
from tests.helpers import initialize_category_records


def test_create_item_successfully(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    new_item = {"name": "item3", "description": "bla blo3"}
    category_id = test_db["categories"][0].id
    response = client.post(
        f"/categories/{category_id}/items",
        json=new_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 200


@pytest.mark.parametrize(
    "item",
    [
        {"name": "test-item1", "description": ""},
        {"name": "", "description": "bla blo"},
        {"name": "", "description": ""}
        # more test cases here
    ],
)
def test_create_item_with_invalid_data(client, item):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    category_id = test_db["categories"][0].id
    response = client.post(
        f"/categories/{category_id}/items",
        json=item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 400


def test_create_item_with_existed_name(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    category_id = test_db["categories"][0].id
    new_item = {"name": "item1", "description": "bla blo3"}
    response = client.post(
        f"/categories/{category_id}/items",
        json=new_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 400


def test_create_item_with_unknown_category_id(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    category_id = 100000  # random category id
    new_item = {"name": "item1", "description": "bla blo3"}
    response = client.post(
        f"/categories/{category_id}/items",
        json=new_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 404
