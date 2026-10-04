from fastapi import Depends, status
from fastapi.routing import APIRouter

from app.dependencies.auth.auth_dependencies import get_auth_service

from app.http.requests.auth.logout_request import LogoutRequest
from app.http.requests.auth.refresh_token_request import RefreshTokenRequest
from app.http.requests.auth.user_login_request import UserLoginRequest
from app.http.requests.auth.user_register_request import UserRegisterRequest
from app.http.responses.auth.refresh_token_response import RefreshTokenResponse
from app.http.responses.auth.user_registered_response import UserRegisteredResponse
from app.http.responses.auth.user_login_response import UserLoginResponse
from app.http.responses.auth.logout_response import LogoutResponse
from app.services.auth.auth_service import AuthService


router = APIRouter(prefix='/auth')

@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
)
def register(request: UserRegisterRequest,service: AuthService = Depends(get_auth_service)) -> UserRegisteredResponse:
    service.register(request.create_dto())

    return UserRegisteredResponse(
        code=status.HTTP_201_CREATED,
        message='Пользователь успешно создан',
    )

@router.post('/login')
def login(request: UserLoginRequest, service: AuthService = Depends(get_auth_service)) -> UserLoginResponse:
    tokens = service.login(request.create_dto())

    return UserLoginResponse.model_validate(tokens, from_attributes=True)

@router.post('/refresh')
def refresh(request: RefreshTokenRequest, service: AuthService = Depends(get_auth_service)) -> RefreshTokenResponse:
    tokens = service.refresh_session(request.refresh_token)

    return RefreshTokenResponse.model_validate(tokens, from_attributes=True)

@router.post('/logout')
def logout(request: LogoutRequest, service: AuthService = Depends(get_auth_service)) -> LogoutResponse:
    service.logout(request.refresh_token)

    return LogoutResponse(
        code=status.HTTP_200_OK,
        message='Успех'
    )
