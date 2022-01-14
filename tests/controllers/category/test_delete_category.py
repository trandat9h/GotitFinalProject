from main.libs import generate_token
from main.models.category import Category


def test_delete_category_successfully(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    category_id = test_db["categories"][0].id
    category_name = test_db["categories"][0].name
    response = client.delete(
        f"/categories/{category_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 200
    assert Category.query.filter_by(name=category_name).one_or_none() is None


def test_delete_category_with_no_exist_id(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    category_id = 100000  # random number

    response = client.delete(
        f"/categories/{category_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 404
    assert Category.query.get(category_id) is None


def test_delete_category_with_unauthorized_user(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][1].id
    category_id = test_db["categories"][0].id
    category_name = test_db["categories"][0].name

    response = client.delete(
        f"/categories/{category_id}",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 403
    assert Category.query.filter_by(name=category_name) is not None
