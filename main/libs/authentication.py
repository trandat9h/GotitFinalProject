import hashlib

import jwt

from main import app


def generate_hashed_password(password, salt):
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 100000
    )

    return hashed_password.hex()


def generate_token(user_id):
    encoded_jwt = jwt.encode(
        {"user_id": user_id}, key=app.config["SECRET_KEY"], algorithm="HS256"
    )
    return encoded_jwt
