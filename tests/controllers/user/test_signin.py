import pytest
from flask import json


@pytest.mark.parametrize(
    "test_user",
    [
        {"email": "dat"},
        {"password": ""},
        {},
    ],
)
def test_signin_with_missing_data(client, test_user, initialize_records):
    response = client.post("/users/signin", json=test_user)
    assert response.status_code == 400


def test_signin_with_incorrect_data(client, initialize_records):
    test_user = {"email": "dat1@gmail.com", "password": "Dat12345678"}
    response = client.post("/users/signin", json=test_user)

    assert response.status_code == 400


def test_signin_successfully(client, initialize_records):
    test_user = {"email": "dat1@gmail.com", "password": "Dat1234"}
    response = client.post("/users/signin", json=test_user)
    json_response = json.loads(response.data)

    assert response.status_code == 200
    assert json_response["access_token"] is not None
