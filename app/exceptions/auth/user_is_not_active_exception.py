from app.exceptions.app_exception import AppException


class UserIsNotActiveException(AppException):
    code = 401
    message = 'Действие учётной записи приостановлено'