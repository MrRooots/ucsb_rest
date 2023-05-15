import json

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest

from src.core.repository import CurrencyRepository

INVALID_FORMAT_ERROR = (
  'Invalid currencies format! Required format is: '
  '"currencies": {'
  '"CURRENCY_NAME": {'
  '"ANOTHER_CURRENCY_NAME": EXCHANGE_RATE,...'
  '}, ...'
  '}'
)


class DatabaseView(web.View):
  """
  View handles '/database' url
  """

  async def post(self) -> web.Response:
    """
    POST method handler
    Request body:
      {
        "merge": int { 1 | 0 }  <- Rewrite whole table if merge == 0
        "currencies": {
          "CURRENCY_NAME": {
            "ANOTHER_CURRENCY_NAME": EXCHANGE_RATE,
            ...
          },
          ...
        }
      }
    """
    print(f'[DatabaseView.post]:', self.request)

    try:
      post_params = await self.request.json()
      query_params = ['merge', 'currencies']
      params = [post_params.get(p) for p in query_params]
    except (ValueError, AttributeError):
      raise HTTPBadRequest(text=json.dumps({
        'success': 0,
        'error': '400 Bad Request',
        'description': INVALID_FORMAT_ERROR
      }), headers={'Content-Type': 'Application/json'})

    if not all(i is not None and i != {} for i in params):
      raise HTTPBadRequest(text=json.dumps({
        'success': 0,
        'error': '400 Bad Request',
        'description': f'Not all required params are specified. [merge={params[0]}, currencies={params[1]}]'
      }), headers={'Content-Type': 'Application/json'})
    elif not all(isinstance(val, dict) for val in params[-1].values()):
      raise HTTPBadRequest(text=json.dumps({
        'success': 0,
        'error': '400 Bad Request',
        'description': INVALID_FORMAT_ERROR
      }), headers={'Content-Type': 'Application/json'})

    return web.json_response(text=json.dumps({
      'success': 1,
      'conversion': {
        'data': {query_params[i]: params[i] for i in range(len(query_params))},
        'result': await CurrencyRepository.update_currencies(self.request.app, *params)
      }
    }))
