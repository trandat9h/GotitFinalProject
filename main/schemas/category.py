from marshmallow import fields, validate

from .base import BaseSchema


class CategorySchema(BaseSchema):
    id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=1))
