import pytest

from main.libs import generate_token
from main.models.item import Item


def test_update_item_successfully(client, initialize_records):
    test_db = initialize_records

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
    updated_item = Item.query.get(item_id)
    assert (
        updated_item.name == update_item["name"]
        and updated_item.description == update_item["description"]
    )


def test_update_item_with_existed_item_name(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    item_id = test_db["items"][0].id
    item_name = test_db["items"][0].name
    category_id = test_db["categories"][0].id
    update_item = {
        "name": test_db["items"][1].name,
        "description": "bla blo3",
    }  # item name existed

    response = client.put(
        f"/categories/{category_id}/items/{item_id}",
        json=update_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 400
    assert Item.query.get(item_id).name == item_name


def test_update_item_with_unknown_category_id(client, initialize_records):
    test_db = initialize_records

    user_id = test_db["users"][0].id
    item_id = test_db["items"][0].id
    update_item = {"name": "item3", "description": "bla blo3"}
    category_id = 100000  # random category_id

    response = client.put(
        f"/categories/{category_id}/items/{item_id}",
        json=update_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )
    json_response = response.get_json()

    assert response.status_code == 404
    assert json_response["error_message"] == "Category not found."
    assert Item.query.filter_by(category_id=category_id).one_or_none() is None


def test_update_item_with_unknown_item_id(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    item_id = 100000  # random item_id
    update_item = {"name": "item3", "description": "bla blo3"}
    category_id = test_db["categories"][0].id
    response = client.put(
        f"/categories/{category_id}/items/{item_id}",
        json=update_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )
    json_response = response.get_json()

    assert response.status_code == 404
    assert json_response["error_message"] == "Item not found."
    assert Item.query.get(item_id) is None


def test_update_item_with_unauthorized_user(client, initialize_records):
    test_db = initialize_records

    user_id = 100000  # random user_id
    item_id = test_db["items"][0].id
    item_name = test_db["items"][0].name
    item_description = test_db["items"][0].description
    update_item = {"name": "item3", "description": "bla blo3"}
    category_id = test_db["categories"][0].id

    response = client.put(
        f"/categories/{category_id}/items/{item_id}",
        json=update_item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 403
    updated_item = Item.query.get(item_id)
    assert (
        updated_item.name == item_name and updated_item.description == item_description
    )


@pytest.mark.parametrize(
    "item",
    [
        {"name": "test-item1", "description": ""},
        {"name": "", "description": "bla blo"},
        {"name": "", "description": ""},
        {"name": ""},
        {"description": ""},
        {},
    ],
)
def test_update_item_with_invalid_data(client, item, initialize_records):
    test_db = initialize_records

    user_id = test_db["users"][0].id
    item_id = test_db["items"][0].id
    category_id = test_db["categories"][0].id
    item_name = test_db["items"][0].name
    item_description = test_db["items"][0].description

    response = client.put(
        f"/categories/{category_id}/items/{item_id}",
        json=item,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 400
    updated_item = Item.query.get(item_id)
    assert (
        updated_item.name == item_name and updated_item.description == item_description
    )
