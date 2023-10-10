from flask import Flask
from dotenv import dotenv_values
# from utils.connections import mongo, redis, socket_
# from src.services.routes import register_endpoints
# from src.services.events import register_socket_events
import asyncio


async def init(app):
    app.config.update(dotenv_values())

    # socket = app.SocketIO = socket_(app)
    # app.db = mongo(app)
    # app.redis = redis(app)

    # await register_endpoints(app)
    # await register_socket_events(socket)
    return app


app = Flask(__name__)

with app.app_context():
    server = asyncio.run(init(app))
    server.run(
    debug=False,
    host=server.config["HOST"],
    port=int(server.config["PORT"]),
    # allow_unsafe_werkzeug=True,
)
