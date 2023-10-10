import jwt
import os
from uuid import uuid4
from flask import current_app
from cryptography.fernet import Fernet

app = current_app
key = b"O84hRkzml1lvq1fu-rtV7LbGAKkPoXqsyNu6hnCsJYY="


def create_token(payload):
    return jwt.encode(payload, app.config["JWT_SECRET"], algorithm="HS256")


def save_token(token):
    key = f"USER:{uuid4()}"
    app.redis.setex(key, int(app.config["REDIS_EXPIRY"]), token)
    return key


def delete_token(app, token):
    is_deleted = app.redis.delete(token)
    if is_deleted:
        return True
    return False


def verify_token(jwt_):
    return jwt.decode(jwt_, app.config["JWT_SECRET"], algorithms=["HS256"])


def encrypt(token):
    f = Fernet(key)
    return f.encrypt(token.encode("utf-8"))


def decrypt(token):
    token = token.split("'")[1].encode("utf-8")
    f = Fernet(key)
    return f.decrypt(token)
