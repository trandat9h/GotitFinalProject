from main.libs.authentication import generate_hashed_password
from main.models.user import User


def get_user_by_email_and_password(email, password):
    user = User.query.filter_by(email=email).one_or_none()

    if user:
        hashed_password = generate_hashed_password(password, user.salt)
        if hashed_password != user.hashed_password:
            return None

    return user
