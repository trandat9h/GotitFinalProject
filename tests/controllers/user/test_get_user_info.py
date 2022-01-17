from main.libs import generate_token


def test_get_user_info_successfully(client, initialize_records):
    test_db = initialize_records
    user_id = test_db["users"][0].id
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {generate_token(user_id)}"},
    )
    assert response.status_code == 200


def test_get_user_info_with_no_header(client, initialize_records):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_get_user_info_with_invalid_header(client, initialize_records):
    response = client.get("/users/me", headers={"Authorization": "Bearer"})
    assert response.status_code == 401
