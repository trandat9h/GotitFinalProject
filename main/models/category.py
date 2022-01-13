from main import db

from .model_mixin import ModelMixin


class Category(ModelMixin, db.Model):
    __tablename__ = "category"

    name = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    items = db.relationship("Item", cascade="all, delete", lazy="dynamic")

    #  mixin flask python
