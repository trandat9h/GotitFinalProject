import functools

import jwt
from flask import request
from marshmallow import ValidationError as MarshmallowValidationError

from main import app
from main.commons.exceptions import (
    CategoryNotFound,
    ItemNotFound,
    Unauthorized,
    ValidationError,
)
from main.models.category import Category


def check_category_exist(func):
    @functools.wraps(func)
    def wrapper_function(*args, **kwargs):
        category_id = kwargs["category_id"]
        category = Category.query.get(category_id)

        if category is None:
            raise CategoryNotFound()

        kwargs["category"] = category
        return func(*args, **kwargs)

    return wrapper_function


def check_item_exist(func):
    @functools.wraps(func)
    def wrapper_function(*args, category, item_id, **kwargs):
        item = category.items.filter_by(id=item_id).one_or_none()

        if item is None:
            raise ItemNotFound()

        kwargs["item"] = item
        return func(*args, **kwargs)

    return wrapper_function


def validate_input(schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if request.method in ["GET", "DELETE"]:
                data = request.args
            else:
                data = request.get_json()

            try:
                loaded_data = schema().load(data)
            except MarshmallowValidationError as e:
                raise ValidationError(error_data=e.messages)
            return func(*args, **loaded_data, **kwargs)

        return wrapper

    return decorator


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
        except (jwt.InvalidTokenError, KeyError, IndexError):
            raise Unauthorized()

    return wrapper
