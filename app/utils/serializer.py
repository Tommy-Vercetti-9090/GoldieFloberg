import datetime
from bson.objectid import ObjectId
import json
from bson.dbref import DBRef
import mongoengine


class MongoJsonEncoder(json.JSONEncoder):
    """."""

    def default(self, obj):
        """."""
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, (ObjectId)):
            return str(obj)
        elif isinstance(obj, (DBRef)):
            return str(obj.id)

        return json.JSONEncoder.default(self, obj)


class Serializer:
    """."""

    def __init__(self, app):
        """."""
        self.app = app

    def jsonify(self, args, *kwargs):
        """Function jsonify with support for MongoDB ObjectId."""
        indent = None
        separators = (",", ":")

        if self.app.config["JSONIFY_PRETTYPRINT_REGULAR"] or self.app.debug:
            indent = 2
            separators = (", ", ": ")

        if args and kwargs:
            raise TypeError(
                "jsonify() behavior undefined when passed both args and kwargs"
            )
        elif len(args) == 1:  # single args are passed directly to dumps()
            data = args

        else:
            data = args or kwargs

        if isinstance(data, mongoengine.queryset.QuerySet):
            # Convert the QuerySet to a list of dictionaries
            data = [doc.to_dict() for doc in data]

            return self.app.response_class(
                (
                    json.dumps(
                        data, indent=indent, separators=separators, cls=MongoJsonEncoder
                    ),
                    "\n",
                ),
                mimetype=self.app.config["JSONIFY_MIMETYPE"],
            )

        return self.app.response_class(
            (
                json.dumps(
                    data, indent=indent, separators=separators, cls=MongoJsonEncoder
                ),
                "\n",
            ),
            mimetype=self.app.config["JSONIFY_MIMETYPE"],
        )
