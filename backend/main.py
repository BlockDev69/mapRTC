from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
from uuid import UUID

from router import home, session
from redis_client import get_redis_client, close_redis_client
from services import auth
from services.redis_backend import RedisBackend
from models.session import Session

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = await get_redis_client()
    try:
        await redis_client.ping()
        print("Connected to Redis successfully!")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        raise

    auth.backend = RedisBackend[UUID, Session](
        session_model=Session, 
        redis=redis_client, 
        prefix="session"
    )
    print("Redis backend for sessions initialized.")

    auth.verifier = auth.SessionVerifierImpl(
        identifier="general_verifier",
        auto_error=False,
        backend=auth.backend,
        auth_http_exeption=auth.HTTPException(status_code=403, detail="No valid session found"),
    )
    print("Session verifier initialized.")

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

app.include_router(router=home.router)
app.include_router(router=session.router)

#FOR DEBUG
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
