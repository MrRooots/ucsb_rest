import json

import aioredis
from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound

from src.utils.utils import Utils


class CurrencyRepository:
  """
  Repository works with raw data and database.
  """

  @staticmethod
  async def convert_currencies(app: web.Application,
                               c_from: str,
                               c_to: str,
                               amount: float) -> float:
    from_data, to_data = await app['redis'].hmget('currencies', c_from, c_to)

    if from_data is None and to_data is None:
      raise HTTPNotFound(text=json.dumps({
        'success': 0,
        'error': '404 Not Found',
        'description': f'No values for given currencies found in the database'
      }), headers={'Content-Type': 'Application/json'})

    if from_data is not None:
      from_data = json.loads(from_data)

    if to_data is not None:
      to_data = json.loads(to_data)

    if from_data and c_to in from_data:
      # Required exchange rate is in requested `from` currency
      exchange_rate = from_data[c_to]
    elif to_data and c_from in to_data:
      # [REVERSE] Required exchange rate for requested `from` currency is in `to` currency
      exchange_rate = 1 / to_data[c_from]
    else:
      raise HTTPNotFound(text=json.dumps({
        'success': 0,
        'error': '404 Not Found',
        'description': f'No data for [{c_from if not from_data else c_to}] currency found in the database'
      }), headers={'Content-Type': 'Application/json'})

    return round(float(amount) * exchange_rate, 2)

  @staticmethod
  async def update_currencies(app: web.Application,
                              merge: int,
                              currencies: dict[str, dict[str: float]]) -> str:
    """ Update or rewrite currencies in DB """
    redis: aioredis.Redis = app['redis']

    if merge == 0:
      await app['redis'].delete('currencies')
    else:
      # Save existing exchange rates [May be slow for large data]
      data = zip(currencies.keys(),
                 await redis.hmget('currencies', keys=list(currencies.keys())))

      currencies = Utils.merge_dicts(currencies,
                                     {k: json.loads(d) for k, d in data})

    await redis.hset('currencies',
                     mapping={k: json.dumps(v) for (k, v) in currencies.items()})

    return 'Updated'
