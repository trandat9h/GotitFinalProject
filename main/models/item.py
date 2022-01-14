from main import db

from .model_mixin import ModelMixin


class Item(ModelMixin, db.Model):
    __tablename__ = "item"

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
