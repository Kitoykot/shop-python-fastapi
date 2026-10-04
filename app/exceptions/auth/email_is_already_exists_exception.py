from app.exceptions.app_exception import AppException


class EmailIsAlreadyExists(AppException):
    code = 409
    message = 'Пользователь с таким email уже существует'
