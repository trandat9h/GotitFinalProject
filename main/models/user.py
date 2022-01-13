from main import db

from .model_mixin import ModelMixin


class User(db.Model, ModelMixin):
    __tablename__ = "user"

    email = db.Column(db.String(45), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), unique=True, nullable=False)
    salt = db.Column(db.String(64), unique=True, nullable=False)
    category = db.relationship("Category")
    item = db.relationship("Item")
