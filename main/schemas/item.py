from marshmallow import fields, post_load, validate, validates

from .base import BaseSchema


class ItemSchema(BaseSchema):
    id = fields.Integer()
    user_id = fields.Integer()
    category_id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(required=True, validate=validate.Length(min=1, max=100))

    @validates("name")
    def name_validator(self, value):
        self.ascii_validator(value)

    @validates("description")
    def description_validator(self, value):
        self.ascii_validator(value)

    @post_load
    def strip_data(self, data, **__):
        data["description"] = data["description"].strip()
        data["name"] = data["name"].strip()
        return data
