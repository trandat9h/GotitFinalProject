from main.libs import generate_token
from tests.helpers import initialize_category_records


def test_delete_item_successfully(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    item_id = test_db["items"][0].id
    category_id = test_db["categories"][0].id
    response = client.delete(
        f"/categories/{category_id}/items/{item_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 200


def test_delete_item_with_unknown_category_id(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    item_id = test_db["items"][0].id
    category_id = 100000  # random category_id
    response = client.delete(
        f"/categories/{category_id}/items/{item_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 404


def test_delete_item_with_unknown_item_id(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    item_id = 100000  # random category_id
    category_id = test_db["categories"][0].id
    response = client.delete(
        f"/categories/{category_id}/items/{item_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 404


def test_delete_item_with_unauthorized_user(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][1].id
    item_id = test_db["items"][0].id
    category_id = test_db["categories"][0].id
    response = client.delete(
        f"/categories/{category_id}/items/{item_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 403
