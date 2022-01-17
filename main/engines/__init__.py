import hashlib

from main.models.user import User


def get_user_by_email_and_password(email, password):
    user = User.query.filter_by(email=email).one_or_none()

    if user:
        hashed_password = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytearray.fromhex(user.salt), 100000
        ).hex()
        if hashed_password != user.hashed_password:
            return None

    return user
