from utils.response import CustomErrorHandler
from flask import request
from utils.token import decrypt, verify_token
from bson.objectid import ObjectId
import jwt


def check_auth():
    try:
        if not request.headers.get('authorization'):
            return CustomErrorHandler({"message": "Token not found", "status": 403}, 403)

        token = decrypt(request.headers.get(
            'authorization').split(" ")[1]).decode('utf8')

        payload = verify_token(token)

        print('payload', payload)
        request.user_id = ObjectId(payload['_id'])
        return

    except jwt.ExpiredSignatureError as e:
        return CustomErrorHandler({"message": "Token expired"}, 401)

    except Exception as e:
        return CustomErrorHandler(e.args[0], 500)
