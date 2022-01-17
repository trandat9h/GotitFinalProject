from main.libs import generate_token
from main.models.item import Item


def test_delete_item_successfully(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    item_id = test_db["items"][0].id
    item_name = test_db["items"][0].name
    category_id = test_db["categories"][0].id
    response = client.delete(
        f"/categories/{category_id}/items/{item_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 200
    assert Item.query.filter_by(name=item_name).one_or_none() is None


def test_delete_item_with_unknown_category_id(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    item_id = test_db["items"][0].id
    item_name = test_db["items"][0].name
    category_id = 100000  # random category_id
    response = client.delete(
        f"/categories/{category_id}/items/{item_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )
    json_response = response.get_json()

    assert response.status_code == 404
    assert json_response["error_message"] == "Category not found."
    assert (
        Item.query.filter_by(name=item_name, category_id=category_id).one_or_none()
        is None
    )


def test_delete_item_with_unknown_item_id(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    item_id = 100000  # random category_id
    category_id = test_db["categories"][0].id
    response = client.delete(
        f"/categories/{category_id}/items/{item_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )
    json_response = response.get_json()

    assert response.status_code == 404
    assert json_response["error_message"] == "Item not found."
    assert Item.query.get(item_id) is None


def test_delete_item_with_unauthorized_user(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][1].id
    item_id = test_db["items"][0].id
    item_name = test_db["items"][0].name
    category_id = test_db["categories"][0].id
    response = client.delete(
        f"/categories/{category_id}/items/{item_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 403
    assert Item.query.filter_by(name=item_name).one_or_none() is not None
