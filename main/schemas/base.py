from flask import jsonify
from marshmallow import EXCLUDE, Schema, ValidationError, fields


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))

    def ascii_validator(self, value):
        for char in value:
            if not char.isascii():
                raise ValidationError("Category name contain non-ascii character.")


class PaginationSchema(BaseSchema):
    items_per_page = fields.Integer()
    page = fields.Integer()
    total_items = fields.Integer()
