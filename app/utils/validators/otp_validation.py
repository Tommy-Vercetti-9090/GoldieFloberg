from marshmallow import Schema, fields


class VerifyOtp(Schema):
    user_id = fields.String(required=True)
    otp_key = fields.String(required=True)
