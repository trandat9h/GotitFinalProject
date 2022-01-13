import pytest

from main.libs import generate_token
from tests.helpers import initialize_category_records


def test_update_item_successfully(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    item_id = test_db["items"][0].id
    update_item = {"name": "item3", "description": "bla blo3"}
    category_id = test_db["categories"][0].id
    response = client.put(
        f"/categories/{category_id}/items/{item_id}",
        json=update_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 200


def test_update_item_with_unknown_category_id(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    item_id = test_db["items"][0].id
    update_item = {"name": "item3", "description": "bla blo3"}
    category_id = 100000  # random category_id
    response = client.put(
        f"/categories/{category_id}/items/{item_id}",
        json=update_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 404


def test_update_item_with_unknown_item_id(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    item_id = 100000  # random item_id
    update_item = {"name": "item3", "description": "bla blo3"}
    category_id = test_db["categories"][0].id
    response = client.put(
        f"/categories/{category_id}/items/{item_id}",
        json=update_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 404


def test_update_item_with_unauthorized_user(client):
    test_db = initialize_category_records()
    user_id = 100000  # random user_id
    item_id = test_db["items"][0].id
    update_item = {"name": "item3", "description": "bla blo3"}
    category_id = test_db["categories"][0].id
    response = client.put(
        f"/categories/{category_id}/items/{item_id}",
        json=update_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 403


@pytest.mark.parametrize(
    "item",
    [
        {"name": "test-item1", "description": ""},
        {"name": "", "description": "bla blo"},
        {"name": "", "description": ""}
        # more test cases here
    ],
)
def test_update_item_with_invalid_data(client, item):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    item_id = test_db["items"][0].id
    category_id = test_db["categories"][0].id
    response = client.put(
        f"/categories/{category_id}/items/{item_id}",
        json=item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 400
