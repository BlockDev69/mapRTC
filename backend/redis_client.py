from redis.asyncio import Redis
from os import environ as env
from typing import Optional

_redis_client: Optional[Redis] = None

async def get_redis_client() -> Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis(
            host=env.get("REDIS_HOST", 'redis'),
            port=int(env.get("REDIS_PORT", 6379)),
            db=int(env.get("REDIS_DB", 0)),
            password=env.get("REDIS_PASSWORD", None),
            decode_responses=True
    )
    return _redis_client

# redis_client = redis.Redis(
#     host=env.get("REDIS_HOST", 'redis'),
#     port=int(env.get("REDIS_PORT", 6379)),
#     db=int(env.get("REDIS_DB", 0)),
#     password=env.get("REDIS_PASSWORD", None),
#     decode_responses=True
# )

async def close_redis_client():
    global _redis_client
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None