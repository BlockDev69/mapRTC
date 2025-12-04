from uuid import UUID
from fastapi import HTTPException

from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.session_verifier import SessionVerifier

from models.session import Session
from core.config import settings
from services.redis_backend import RedisBackend

cookie_params = CookieParameters()

cookie_handler = SessionCookie(
    cookie_name=settings.SESSION_COOKIE_NAME,
    identifier="general_verifier",
    auto_error=False,
    secret_key=settings.SECRET_KEY,
    cookie_params=cookie_params,
)

backend = None
verifier = None

class SessionVerifierImpl(SessionVerifier[UUID, Session]):
    def __init__(self, *, identifier, auto_error, backend, auth_http_exeption):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exeption = auth_http_exeption
    
    @property
    def identifier(self) -> str:
        return self._identifier
    
    @property
    def auto_error(self) -> bool:
        return self._auto_error
    
    @property
    def backend(self) -> RedisBackend[UUID, Session]:
        return self._backend
    
    @property
    def auth_http_exception(self) -> HTTPException:
        return self._auth_http_exeption