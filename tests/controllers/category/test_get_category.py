def test_get_categories_successfully(client, initialize_records):
    response = client.get("/categories?page=1")
    assert response.status_code == 200


def test_get_categories_with_no_page_params(client, initialize_records):
    response = client.get("/categories")  # no page params provided
    assert response.status_code == 400


def test_get_categories_with_no_items_page(client, initialize_records):
    response = client.get("/categories?page=100")  # page is too large
    json_response = response.get_json()

    assert response.status_code == 404
    assert json_response["error_code"] == 404001
    assert json_response["error_message"] == "Not found."


def test_get_categories_with_no_invalid_page(client, initialize_records):
    response = client.get("/categories?page=string")  # page is not IntType
    assert response.status_code == 400
