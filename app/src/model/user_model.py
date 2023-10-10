import jsonschema


class User:
    def __init__(self, document):
        self.schema = {
            "type": "object",
            "properties": {
                "user_type": {"type": "string", "enum": ["patient", "admin", "case_manager" ]},
                "email": {"type": "string", "format": "email"},
                "password": {"type": "string"},
                "is_verified": {"type": "boolean"},
                "is_profile_completed": {"type": "boolean"},
            },
            "required": [
                "email",
                "password",
                "user_type",
            ],
        }
        self.document = document

    def __call__(self):
        jsonschema.validate(self.document, self.schema)
