from main.libs import generate_token


def test_get_single_item_successfully(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    category_id = test_db["categories"][0].id
    item_id = test_db["items"][0].id
    response = client.get(
        f"/categories/{category_id}/items/{item_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 200


def test_get_single_item_with_unknown_item_id(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    category_id = test_db["categories"][0].id
    item_id = 100000  # random item_id
    response = client.get(
        f"/categories/{category_id}/items/{item_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 404


def test_get_single_item_with_unknown_category_id(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    category_id = 100000  # random item_id
    item_id = test_db["items"][0].id
    response = client.get(
        f"/categories/{category_id}/items/{item_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 404


def test_get_all_items_successfully(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    category_id = test_db["categories"][0].id
    response = client.get(
        f"/categories/{category_id}/items?page=1",  # test page is 1 by default
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 200


def test_get_all_items_with_unknown_category_id(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    category_id = 100000  # random category_id
    response = client.get(
        f"/categories/{category_id}/items",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 404
