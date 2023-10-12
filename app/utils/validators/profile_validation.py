from marshmallow import Schema, fields, validate


class CreateProfile(Schema):
    name = fields.String(required=True)
    preferred_name = fields.String(required=True)
    phone = fields.String(required=True)
    dob = fields.String(required=True)
    address = fields.String(required=True)
