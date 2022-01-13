from main.libs import generate_token
from tests.helpers import initialize_category_records


def test_get_categories_successfully(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    response = client.get(
        "/categories?page=1",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )
    assert response.status_code == 200


def test_get_categories_with_invalid_authentication(client):
    _ = initialize_category_records()
    response = client.get(
        "/categories?page=1",
        headers={"Authorization": "unknown header"},
    )
    assert response.status_code == 401


def test_get_categories_with_no_authentication(client):
    _ = initialize_category_records()
    response = client.get("/categories?page=1")
    assert response.status_code == 401