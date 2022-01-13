import pytest
from flask import json

from tests.helpers import initialize_user_records


@pytest.mark.parametrize(
    ("email", "password", "message"),
    (
        ("dat@gmail.com", "1", "Shorter than minimum length 6."),
        ("dat@gmail.com", "da123", "Shorter than minimum length 6."),
        ("dat@gmail.com", "dat123", "Password contains no uppercase character."),
        ("dat@gmail.com", "Datttttt", "Password contains no number."),
        ("dat@gmail.com", "DATTTTT", "Password contains no lowercase character."),
        # more test case
    ),
)
def test_signup_with_invalid_data(client, email, password, message):
    response = client.post("/users/signup", json={"email": email, "password": password})
    json_response = json.loads(response.data)
    assert json_response["error_code"] == 400000


def test_signup_with_existed_email(client):
    _ = initialize_user_records()
    signup_user = {"email": "dat1@gmail.com", "password": "Dat12345"}
    response = client.post("/users/signup", json=signup_user)

    assert response.status_code == 400


def test_signup_successfully(client):
    signup_user = {"email": "dat@gmail.com", "password": "Dat12345"}
    response = client.post("/users/signup", json=signup_user)

    assert response.status_code == 200
