from flask import jsonify

from main import app, db
from main.commons.decorators import validate_input, validate_token
from main.commons.exceptions import EmailExisted, LoginUnsuccessfully
from main.engines import get_user_by_email_and_password
from main.libs import generate_hashed_password, generate_token
from main.models.user import User
from main.schemas.user import UserSchema


@app.post("/users/sign-in")
@validate_input(UserSchema)
def sign_in(email, password, **__):
    user = get_user_by_email_and_password(email, password)
    if user is None:
        raise LoginUnsuccessfully()

    return jsonify({"access_token": generate_token(user.id)})


@app.post("/users/signup")
@validate_input(UserSchema)
def signup(email, password, **__):
    existing_user = User.query.filter_by(email=email).one_or_none()
    if existing_user:
        raise EmailExisted()

    hashed_password, salt = generate_hashed_password(password)
    new_user = User(email=email, hashed_password=hashed_password, salt=salt)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(
        {"user_id": new_user.id, "access_token": generate_token(new_user.id)}
    )


@app.get("/users/me")
@validate_token
def get_profile(user_id, **__):
    user = User.query.get(user_id)

    return jsonify({"user_id": user_id, "email": user.email})
