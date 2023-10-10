from flask import Flask
from dotenv import dotenv_values
from utils.connections import mongo
from src.services.routes import register_endpoints
import asyncio


async def init(app):
    app.config.update(dotenv_values())
    app.db = mongo(app)
    await register_endpoints(app)
    return app


app = Flask(__name__)

with app.app_context():
    server = asyncio.run(init(app))
    server.run(
        debug=False,
        host=server.config["HOST"],
        port=int(server.config["PORT"]),
    )
