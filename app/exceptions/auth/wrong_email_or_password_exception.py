from app.exceptions.app_exception import AppException


class WrongEmailOrPasswordException(AppException):
    code = 401
    message = 'Неверный логин или пароль'
