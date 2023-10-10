from pymongo import MongoClient
from logger.config import logger
from .db_indexes import indexes
# from flask_socketio import socketio, emit
# from flask_socketio import SocketIO


def mongo(server):
    mongo_client = MongoClient(server.config["MONGODB_URI"])
    logger.info("Connected to database {}".format(mongo_client))
    db = mongo_client[server.config["MONGODB_DATABASE"]]
    indexes(db)
    return db


# def redis(server):
#     r = Redis(
#         host=server.config["REDIS_HOST"],
#         port=int(server.config["REDIS_PORT"]),
#         # decode_responses=True,
#     )
#     logger.info(
#         "Connected to redis at {}:{}".format(
#             server.config["REDIS_HOST"], server.config["REDIS_PORT"]
#         )
#     )
#     return r
