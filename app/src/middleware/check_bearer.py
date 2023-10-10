from utils.response import CustomErrorHandler
from flask import request, current_app
import os


async def check_bearer():
    app = current_app
    token = request.headers.get("bearer-token")
    try:
        if token == app.config["BEARER_TOKEN"]:
            return
        else:
            raise Exception({"message": "Invalid Token", "status": 404})
    except Exception as e:
        return CustomErrorHandler(e.args[0], 500)
