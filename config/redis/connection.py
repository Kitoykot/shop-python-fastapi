from config.redis.settings import redis_settings
from redis import Redis

client = Redis(
    host=redis_settings.redis_host,
    port=redis_settings.redis_port,
    db=redis_settings.redis_db,
    decode_responses=True,
)
