from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from router import home
from redis_client import get_redis_client, close_redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = await get_redis_client()
    try:
        await redis_client.ping()
        print("Connected to Redis successfully!")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        raise
    yield
    await close_redis_client()
    print("Redis connection closed.")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000",
                   "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home.router)

@app.get("/health")
async def health_check(redis_client: Redis = Depends(get_redis_client)) -> dict:
    try:
        pong = await redis_client.ping()
        if pong:
            return {"status": "healthy", "redis": "connected"}
        else:
            return {"status": "unhealthy", "redis": "not connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# @app.on_event("startup")
# async def startup_event():
#     redis_client = get_redis_client()
#     try:
#         redis_client.ping()
#         print("Connected to Redis successfully!")
#     except Exception as e:
#         print(f"Failed to connect to Redis: {e}")
#     finally:
#         redis_client.close()
