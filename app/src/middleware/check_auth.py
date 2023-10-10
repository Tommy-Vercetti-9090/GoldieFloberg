from utils.response import CustomErrorHandler
from flask import request, current_app
from utils.token import decrypt, verify_token
from bson.objectid import ObjectId

def check_auth():
    try:
        app = current_app
        token = request.headers.get('authorization').split(" ")[1]
        if not token:
            raise Exception({"message": "Token not found" , "status": 404})
        token = decrypt(token).decode('utf8')
        jwt_token = app.redis.get(token)
        if not jwt_token:
            raise Exception({"message": "Token expired in redis" , "status": 404})
        payload = verify_token(jwt_token)
        request.user_id = ObjectId(payload['_id'])
        return

    except Exception as e:
        return CustomErrorHandler(e.args[0], 500)