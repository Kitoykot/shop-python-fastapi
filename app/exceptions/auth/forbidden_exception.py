from app.exceptions.app_exception import AppException


class ForbiddenException(AppException):
    message = 'Доступ запрещен'
    code = 403
