from marshmallow import Schema, fields

class UserSignUp(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    user_type = fields.String(required=True)