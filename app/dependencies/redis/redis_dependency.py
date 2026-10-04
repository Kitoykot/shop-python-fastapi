from redis import Redis

from config.redis.connection import client


def get_redis() -> Redis:
    return client
