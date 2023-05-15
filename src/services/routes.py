from aiohttp import web

from src.views.convert_view import ConvertView
from src.views.database_view import DatabaseView


class Routes:
  @staticmethod
  def register_routes(app: web.Application) -> None:
    """ Register routes for given `app`  """
    app.add_routes([
      web.get('/convert', ConvertView),
      web.post('/database', DatabaseView)
    ])
