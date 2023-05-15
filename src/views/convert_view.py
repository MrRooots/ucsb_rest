import json

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest

from src.core.repository import CurrencyRepository


class ConvertView(web.View):
  """
  View handles '/convert' url
  """

  async def get(self) -> web.Response:
    """ GET method handler  """
    print(f'[ConvertView.get]:', self.request)
    query_params = ['from', 'to', 'amount']
    params = [self.request.rel_url.query.get(p) for p in query_params]

    if not all(i is not None and i != '' and i != {} for i in params):
      raise HTTPBadRequest(text=json.dumps({
        'success': 0,
        'error': '400 Bad Request',
        'description': f'Not all required params are specified. [from={params[0]}, to={params[1]}, amount={params[2]}]'
      }), headers={'Content-Type': 'Application/json'})

    return web.json_response(text=json.dumps({
      'success': 1,
      'conversion': {
        'data': {query_params[i]: params[i] for i in range(3)},
        'result': await CurrencyRepository.convert_currencies(self.request.app, *params)
      }
    }))

  def _raise_allowed_methods(self) -> None:
    print('Checking method')
    super(ConvertView, self)._raise_allowed_methods()
