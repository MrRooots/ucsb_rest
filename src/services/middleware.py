import json

from aiohttp import web
from aiohttp.web_exceptions import HTTPMethodNotAllowed, HTTPBadRequest


@web.middleware
async def handle_request_error(request: web.Request, handler: callable):
  try:
    return await handler(request)
  except HTTPMethodNotAllowed:
    return HTTPMethodNotAllowed(
      method=request.method,
      allowed_methods=('GET',),
      headers={'Content-Type': 'Application/json'},
      text=json.dumps({
        'success': 0,
        'error': '405 Method Not Allowed',
        'description': f'Method [{request.method}] not allowed on [{request.path}] route'
      }),
    )
