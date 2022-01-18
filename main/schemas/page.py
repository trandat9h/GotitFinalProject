from marshmallow import fields, validate

from .base import BaseSchema


class PageSchema(BaseSchema):
    page = fields.Integer(
        required=True, validate=validate.Range(min=1), allow_none=False
    )
