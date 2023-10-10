import jsonschema


class Profile:
    def __init__(self, document):
        self.schema = {
            "type": "object",
            "properties": {
                "user_id": {"bsontype": "string"},
                "address": {"type": "string"},
                "country": {"type": "string"},
                "state": {"type": "string"},
                "city": {"type": "string"},
                "phone": {"type": "string"},
                "name": {"type": "string"},
                "profile_picture": {"bsontype": "string"},
            },
            "required": ["user_id", "profile_picture", "name", "phone", "address", "country", "state", "city"],
        }
        self.document = document

    def __call__(self):
        jsonschema.validate(self.document, self.schema)
