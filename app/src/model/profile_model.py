import jsonschema


class Profile:
    def __init__(self, document):
        self.schema = {
            "type": "object",
            "properties": {
                "user_id": {"bsontype": "string"},
                "address": {"type": "string"},
                "phone": {"type": "string"},
                "name": {"type": "string"},
                "preferred_name": {"type": "string"},
                "dob": {"type": "string", "format": "datetime"}
            },
            "required": ["user_id", "name", "preferred_name", "phone", "address", "dob"],
        }
        self.document = document

    def __call__(self):
        jsonschema.validate(self.document, self.schema)
