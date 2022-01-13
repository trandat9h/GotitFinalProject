import pytest

from main.libs import generate_token
from tests.helpers import initialize_category_records


def test_create_category_successfully(client):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    new_category = {"name": "item1"}
    response = client.post(
        "/categories",
        json=new_category,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 200


@pytest.mark.parametrize(
    "category",
    [
        {"name": ""},
        {},
    ],
)
def test_create_category_with_invalid_data(client, category):
    test_db = initialize_category_records()
    user_id = test_db["users"][0].id
    response = client.post(
        "/categories",
        json=category,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 400


def test_create_category_with_existed_name(client):
    test_db = initialize_category_records()
    exist_category = {"name": "category1"}
    user_id = test_db["users"][0].id
    response = client.post(
        "/categories",
        json=exist_category,
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )

    assert response.status_code == 400
