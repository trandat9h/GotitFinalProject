from main.libs import generate_token
from tests.helpers import initialize_category_records


def test_delete_category_successfully(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    category_id = test_db["categories"][0].id
    response = client.delete(
        f"/categories/{category_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 200


def test_delete_category_with_no_exist_id(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    category_id = 100000  # random number

    response = client.delete(
        f"/categories/{category_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 404


def test_delete_category_with_unauthorized_user(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][1].id
    category_id = test_db["categories"][0].id

    response = client.delete(
        f"/categories/{category_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 403
