import asyncio

import aioredis
from aiohttp import web

from src.config.config import Config


class Database:
  @staticmethod
  async def connect(app: web.Application):
    """ Connect to redis database """
    print(f'[Database] Connected to database')
    app['redis']: aioredis.Redis = await aioredis.from_url(Config.DB_HOST,
                                                           encoding=Config.DB_CHARSET)

    yield

    await app['redis'].close()
