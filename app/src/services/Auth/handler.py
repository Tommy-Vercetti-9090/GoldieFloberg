from src.model.user_model import User
from utils.validators.user_validation import UserSignUp
from werkzeug.security import generate_password_hash
from flask import request, current_app
from utils.response import CustomErrorHandler, CustomSuccessHandler

from utils.template import (
    generate_and_save_otp,
    send_mail_template,
    send_email,
)
# from operator import itemgetter
# from utils.token import create_token, save_token, encrypt, decrypt, delete_token
from bson.objectid import ObjectId
# from bson.dbref import DBRef
# import datetime


async def sign_up():
    data = request.json
    try:
        app = current_app
        user_schema = UserSignUp()
        data = user_schema.load(data)
        data["password"] = generate_password_hash(data["password"])

        data.update(
            {
                "createdAt": ObjectId().generation_time,
                "updatedAt": ObjectId().generation_time,
                "is_verified": False,
                "is_profile_completed": False,
            }
        )
        User(data)()
        user_id = app.db["User"].insert_one(data).inserted_id
        if user_id:
            otp_key = generate_and_save_otp(user_id)
            subject, html = send_mail_template(data["email"], otp_key).values()
            await send_email(data["email"], subject, html)

            result = app.db["User"].find_one(
                {"_id": user_id},
                projection={
                    "_id": 1,
                    "email": 1,
                },
            )

        return CustomSuccessHandler(result, "User signed up successfully", 200)

    except Exception as e:
        return CustomErrorHandler({"message": "User already registered"}, 500)\
            if e.code == 11000 else CustomErrorHandler(e.args[0], 500)
