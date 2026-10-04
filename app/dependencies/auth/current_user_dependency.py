from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from app.dependencies.auth.auth_dependencies import get_auth_service

from app.dto.user.user_dto import UserDto
from app.exceptions.auth.unauthorized_exception import UnauthorizedException
from app.services.auth.auth_service import AuthService

bearer = HTTPBearer(auto_error=False)

def get_current_user(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer), 
        auth_service: AuthService = Depends(get_auth_service)
    ) -> UserDto:
        if credentials is None:
            raise UnauthorizedException()

        return auth_service.find_user_by_access_token(credentials.credentials)