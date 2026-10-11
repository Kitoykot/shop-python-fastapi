from redis import Redis
from rq import Queue

from config.redis.settings import redis_settings

client = Redis(
    host=redis_settings.redis_host,
    port=redis_settings.redis_port,
    db=redis_settings.redis_db,
    decode_responses=False,
)

queue = Queue(
    name='notifications',
    connection=client,
)
