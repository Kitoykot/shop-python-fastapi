from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.dependencies.auth.auth_dependencies import get_auth_service
from app.dto.user.read.data.user_data_dto import UserDataDto
from app.exceptions.auth.unauthorized_exception import UnauthorizedException
from app.services.auth.auth_service import AuthService

bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserDataDto:
    if credentials is None:
        raise UnauthorizedException()

    return auth_service.find_user_by_access_token(credentials.credentials)
