import jsonschema


class Media:
    def __init__(self, document):
        self.schema = {
            "type": "object",
            "properties": {
                "media_type": {"type": "string", "enum": ["image", "video"]},
                "url": {"type": "string"},
                "thumbnail": {"type": "string"},
            },
            "required": ["media_type", "url"],
        }
        self.document = document

    def __call__(self):
        jsonschema.validate(self.document, self.schema)
