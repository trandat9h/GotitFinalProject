from marshmallow import fields, validate

from .base import BaseSchema


class ItemSchema(BaseSchema):
    id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(required=True, validate=validate.Length(min=1))
