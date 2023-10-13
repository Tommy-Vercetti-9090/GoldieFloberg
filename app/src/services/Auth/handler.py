from src.model.user_model import User
from utils.validators.user_validation import UserSignUp, UserLogIn
from utils.validators.otp_validation import VerifyOtp
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, current_app
from utils.response import CustomErrorHandler, CustomSuccessHandler

from utils.template import (
    generate_and_save_otp,
    send_mail_template,
    send_email,
)
from operator import itemgetter
from utils.token import create_token, encrypt
from bson.objectid import ObjectId
from bson.dbref import DBRef
from datetime import datetime, timedelta


async def user_signup():
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
        return CustomErrorHandler({"message": "User already registered"}, 400)\
            if e.code == 11000 else CustomErrorHandler(e.args[0], 500)


def user_login():
    data = request.json
    try:
        app = current_app
        user_schema = UserLogIn()
        data = user_schema.load(data)

        user = app.db["User"].find_one(
            {
                "email": data["email"],
                "is_verified": True,
                "user_type": data["user_type"],
            }
        )
        if not user:
            return CustomErrorHandler({"message": "User not found"}, 404)

        if not check_password_hash(user["password"], data["password"]):
            return CustomErrorHandler({"message": "Incorrect password"}, 401)

        token = create_token({"_id": str(
            user["_id"]), "email": user["email"], "exp": datetime.utcnow() + timedelta(hours=int(app.config["TOKEN_EXPIRY_HOURS"]))})
        token = str(encrypt(token))

        return CustomSuccessHandler(
            data={"token": token, "user": user},
            message="User logged in Successfully",
            status=200,
        )

    except Exception as e:
        return CustomErrorHandler(e.args[0], 500)


def verify_otp():
    data = request.json
    try:
        app = current_app
        otp_schema = VerifyOtp()
        data = otp_schema.load(data)

        (otp_key, user_id) = itemgetter("otp_key", "user_id")(data)

        otp = app.db["Otp"].find_one(
            {"user_id": DBRef(collection="User", id=ObjectId(user_id))}
        )

        if datetime.now() > otp["expire_at"]:
            return CustomErrorHandler({"message": "Otp Expired"}, 400)

        elif otp["otp_key"] != otp_key:
            return CustomErrorHandler({"message": "Otp key invalid"}, 400)

        user = app.db["User"].find_one_and_update(
            {"_id": ObjectId(user_id)},
            {
                "$set": {"is_verified": True},
            },
            return_document=True,
            projection={
                "_id": 1,
                "email": 1,
            },
        )
        token = create_token({"_id": str(user["_id"]), "email": user["email"], "exp": datetime.utcnow(
        ) + timedelta(hours=int(app.config["TOKEN_EXPIRY_HOURS"]))})
        # key = save_token(token)
        token = str(encrypt(token))
        return CustomSuccessHandler(
            data={"token": token},
            message="Otp verified Successfully",
            status=200,
        )

    except Exception as e:
        return CustomErrorHandler(e.args[0], 500)
