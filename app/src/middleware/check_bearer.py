from utils.response import CustomErrorHandler
from flask import request, current_app


async def check_bearer():
    app = current_app
    token = request.headers.get("bearer-token")
    try:
        if token == app.config["BEARER_TOKEN"]:
            return
        else:
            return CustomErrorHandler({"message": "Invalid Token", "status": 403}, 403)
    except Exception as e:
        return CustomErrorHandler(e.args[0], 500)
