import pytest
from flask import json

from main.models.user import User


@pytest.mark.parametrize(
    "user",
    [
        {"email": "dat3@gmail.com", "password": "1"},  # password is shorter than 6
        {
            "email": "dat3@gmail.com",
            "password": "dat123",
        },  # password does not contain uppercase letter
        {
            "email": "dat3@gmail.com",
            "password": "Dattttt",
        },  # password does not contain number
        {
            "email": "dat3@gmail.com",
            "password": "DATTTT",
        },  # password does not contain lowercase letter
        {"email": "not email", "password": "Dat1234"},  # email it not in correct form
        {"email": "dat3@gmail.com", "password": ""},  # no password value
        {"email": "", "password": "Dat1234"},  # no email value
        {"email": "", "password": ""},  # no email and password value
        {"password": ""},  # no email field
        {"email": ""},  # no password field
        {
            "email": "Dat5@gmail.com",
            "password": "Dat诶12345",
        },  # password contains non-ascii character
        {},  # no field
    ],
)
def test_signup_with_invalid_data(client, user):
    response = client.post("/users/sign-up", json=user)
    json_response = json.loads(response.data)
    assert json_response["error_code"] == 400000
    assert (
        User.query.filter_by(
            email=user["email"] if "email" in user else None
        ).one_or_none()
        is None
    )


def test_signup_with_existed_email(client, initialize_records):
    signup_user = {"email": "dat1@gmail.com", "password": "Dat12345"}
    response = client.post("/users/sign-up", json=signup_user)

    assert response.status_code == 400
    assert User.query.filter_by(email=signup_user["email"]).one_or_none() is not None


def test_signup_successfully(client, initialize_records):
    signup_user = {"email": "dat3@gmail.com", "password": "Dat12345"}
    response = client.post("/users/sign-up", json=signup_user)

    assert response.status_code == 200
    assert User.query.filter_by(email=signup_user["email"]).one_or_none() is not None
