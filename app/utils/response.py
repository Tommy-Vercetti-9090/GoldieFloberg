from flask import Response, jsonify, current_app
from utils.serializer import Serializer
import json


ser = Serializer(current_app)


def CustomSuccessHandler(data, message, status):
    result = ser.jsonify(data)

    return Response(
        response=json.dumps({"message": message, "data": result.json}),
        status=status,
        mimetype="application/json",
    )


def CustomErrorHandler(message, status):
    status = message["status"] if hasattr(message, "status") else status
    message = message["message"] if hasattr(message, "message") else message
    return Response(
        response=json.dumps({"message": message}),
        status=status,
        mimetype="application/json",
    )
