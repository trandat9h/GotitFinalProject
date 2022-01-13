import functools
import hashlib
import os

import jwt
from flask import request
from marshmallow import ValidationError

from main import app
from main.commons.exceptions import BadRequest, Unauthorized


def generate_hashed_password(password):
    salt = os.urandom(8)
    hashed_password = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)

    return {"hashed_password_with_salt": hashed_password.hex(), "salt": salt.hex()}


def generate_token(user_id):
    encoded_jwt = jwt.encode(
        {"user_id": user_id}, key=app.config["SECRET_KEY"], algorithm="HS256"
    )
    return encoded_jwt


def validate_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers["Authorization"].split(" ")[1]
            header_data = jwt.get_unverified_header(token)
            decoded_data = jwt.decode(
                token, key=app.config["SECRET_KEY"], algorithms=[header_data["alg"]]
            )
            kwargs["user_id"] = decoded_data["user_id"]
            return func(*args, **kwargs)
        except (jwt.InvalidTokenError, KeyError):
            raise Unauthorized(error_message="Unauthenticated.", error_code=401001)

    return wrapper


def validate_input(schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            body = request.get_json()
            try:
                schema().load(body)
            except ValidationError as e:
                raise BadRequest(error_data=dict(e.messages))
            return func(*args, **body, **kwargs)

        return wrapper

    return decorator
