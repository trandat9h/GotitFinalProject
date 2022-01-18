import hashlib
import os

import jwt

from main import app


def generate_hashed_password(password):
    salt = os.urandom(8)
    hashed_password = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)

    return hashed_password.hex(), salt.hex()


def generate_token(user_id):
    encoded_jwt = jwt.encode(
        {"user_id": user_id}, key=app.config["SECRET_KEY"], algorithm="HS256"
    )
    return encoded_jwt
