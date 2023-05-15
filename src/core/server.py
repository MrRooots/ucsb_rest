from aiohttp import web

from src.config.config import Config
from src.services.database import Database
from src.services.middleware import handle_request_error
from src.services.routes import Routes


def start_server() -> None:
  app = web.Application()
  app.cleanup_ctx.append(Database.connect)  # Connect to DB and close connection

  Routes.register_routes(app)

  app.middlewares.append(handle_request_error)

  web.run_app(app, port=Config.SERVER_PORT)
