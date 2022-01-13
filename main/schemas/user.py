from marshmallow import ValidationError, fields, validate, validates

from .base import BaseSchema


class UserSchema(BaseSchema):
    id = fields.Integer()
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))

    @validates("password")
    def password_validator(self, value):
        has_upper = False
        has_lower = False
        has_number = False
        for char in value:
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char.isdecimal():
                has_number = True

        if not has_upper:
            raise ValidationError("Password contains no uppercase character.")
        elif not has_lower:
            raise ValidationError("Password contains no lowercase character.")
        elif not has_number:
            raise ValidationError("Password contains no number.")
