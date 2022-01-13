from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from main import app, db
from main.commons.exceptions import BadRequest, InternalServerError
from main.engines import authenticate_user
from main.libs import (
    generate_hashed_password,
    generate_token,
    validate_input,
    validate_token,
)
from main.models.user import User
from main.schemas.user import UserSchema


@app.post("/users/signin")
@validate_input(UserSchema)
def signin(*_, email, password, **__):
    queried_user = authenticate_user(email, password)
    if queried_user:
        return jsonify({"access_token": generate_token(queried_user.id)}), 200
    else:
        raise BadRequest(error_message="Login Unsuccessfully.", error_code=400006)


@app.post("/users/signup")
@validate_input(UserSchema)
def signup(*_, email, password, **__):
    try:
        existed_user = User.query.filter_by(email=email).one_or_none()
    except SQLAlchemyError as e:
        raise InternalServerError(error_message=str(e))

    if existed_user:
        raise BadRequest(error_message="Email is already existed.", error_code=400010)

    auth_data = generate_hashed_password(password)
    try:
        new_user = User(
            email=email,
            hashed_password=auth_data["hashed_password_with_salt"],
            salt=auth_data["salt"],
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"user_id": new_user.id}), 200
    except Exception as e:
        raise InternalServerError(error_message=str(e))


@app.get("/users/me")
@validate_token
def get_profile(*_, user_id, **__):
    try:
        user = User.query.get(user_id).one()
    except SQLAlchemyError as e:
        raise InternalServerError(error_message=str(e))

    return jsonify({"user_id": user_id, "email": user.email}), 200
