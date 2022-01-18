from marshmallow import fields, post_load, validate, validates

from .base import BaseSchema


class CategorySchema(BaseSchema):
    id = fields.Integer()
    user_id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))

    @post_load
    def strip_data(self, data, **__):
        data["name"] = data["name"].strip()
        return data

    @validates("name")
    def name_validator(self, value):
        self.ascii_validator(value)
