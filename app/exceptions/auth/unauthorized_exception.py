from app.exceptions.app_exception import AppException


class UnauthorizedException(AppException):
    code = 401
    message = 'Ошибка авторизации'
