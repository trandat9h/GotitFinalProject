import functools
import hashlib

from sqlalchemy.exc import NoResultFound

from main.commons.exceptions import BadRequest, InternalServerError, NotFound
from main.models.category import Category
from main.models.user import User


def check_category_exist(func):
    @functools.wraps(func)
    def wrapper_function(*args, **kwargs):
        category_id = kwargs["category_id"]
        try:
            queried_category = Category.query.get(category_id)
        except Exception as e:
            raise InternalServerError(error_message=str(e))

        if queried_category is None:
            raise NotFound(error_message="Category not found.", error_code=404001)

        kwargs["category"] = queried_category
        return func(*args, **kwargs)

    return wrapper_function


def check_item_exist(func):
    @functools.wraps(func)
    def wrapper_function(*args, category, item_id, **kwargs):
        # maybe try another query?
        print(category.items)
        try:
            queried_item = category.items.filter_by(id=item_id).one_or_none()
        except Exception as e:
            raise InternalServerError(error_message=str(e))

        if queried_item is None:
            raise NotFound(error_message="Item not found.", error_code=404001)

        kwargs["item"] = queried_item
        return func(*args, **kwargs)

    return wrapper_function


def authenticate_user(email, password):
    try:
        queried_user = User.query.filter_by(email=email).one()
    except NoResultFound:
        raise BadRequest(error_message="Login Unsuccessfully.", error_code=400006)
    except Exception as e:
        raise InternalServerError(error_message=str(e))

    input_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytearray.fromhex(queried_user.salt), 100000
    ).hex()
    if input_password == queried_user.hashed_password:
        return queried_user
    else:
        return None
