from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.dependencies.auth.auth_dependencies import get_auth_service

from app.dto.user.user_dto import UserDto
from app.exceptions.app_exception import AppException
from app.exceptions.auth.unauthorized_exception import UnauthorizedException
from app.exceptions.auth.user_is_not_active_exception import UserIsNotActiveException
from app.services.auth.auth_service import AuthService

bearer = HTTPBearer(auto_error=False)

def get_current_user_or_guest(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer), 
        auth_service: AuthService = Depends(get_auth_service)
    ) -> UserDto | None:
        if credentials is None:
            return None

        try:
            return auth_service.find_user_by_access_token(credentials.credentials) 
        except (UnauthorizedException, UserIsNotActiveException):
            return None
        