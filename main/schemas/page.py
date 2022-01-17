from marshmallow import ValidationError, fields, pre_load, validate

from .base import BaseSchema


class PageSchema(BaseSchema):
    page = fields.Integer(required=True, validate=validate.Range(min=1))

    @pre_load
    def page_validator(self, data, **__):
        if data["page"] is None:
            raise ValidationError("Page is not provided")

        try:
            page = int(data["page"])
            data["page"] = page
        except ValueError:
            raise ValidationError("Page is not an integer.")

        return data
