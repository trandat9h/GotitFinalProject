def test_get_single_item_successfully(client, initialize_records):
    test_db = initialize_records
    category_id = test_db["categories"][0].id
    item_id = test_db["items"][0].id
    response = client.get(f"/categories/{category_id}/items/{item_id}")

    assert response.status_code == 200


def test_get_single_item_with_unknown_item_id(client, initialize_records):
    test_db = initialize_records
    category_id = test_db["categories"][0].id
    item_id = 100000  # random item_id
    response = client.get(f"/categories/{category_id}/items/{item_id}")
    json_response = response.get_json()

    assert response.status_code == 404
    assert json_response["error_message"] == "Item not found."


def test_get_single_item_with_unknown_category_id(client, initialize_records):
    test_db = initialize_records
    category_id = 100000  # random item_id
    item_id = test_db["items"][0].id
    response = client.get(f"/categories/{category_id}/items/{item_id}")
    json_response = response.get_json()

    assert response.status_code == 404
    assert json_response["error_message"] == "Category not found."


def test_get_all_items_successfully(client, initialize_records):
    test_db = initialize_records
    category_id = test_db["categories"][0].id
    response = client.get(f"/categories/{category_id}/items?page=1")

    assert response.status_code == 200


def test_get_all_items_with_unknown_category_id(client, initialize_records):
    category_id = 100000  # random category_id
    response = client.get(
        f"/categories/{category_id}/items?page=1"
    )  # default page is 1
    json_response = response.get_json()

    assert response.status_code == 404
    assert json_response["error_message"] == "Category not found."
