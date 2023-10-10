import jsonschema



class Otp:
    def __init__(self, document):
        self.schema = {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "object",
                    "properties": {
                        "$ref": {"type": "string"},
                        "$id": {
                            "bsontype": "string",
                        },
                    },
                },
                "expire_at": {"format": "date"},
                "otp_key": {"type": "string"},
            },
            "required": ["user_id", "otp_key"],
        }
        self.document = document

    def __call__(self):
        jsonschema.validate(self.document, self.schema)
