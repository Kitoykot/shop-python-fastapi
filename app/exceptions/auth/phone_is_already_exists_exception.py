from app.exceptions.app_exception import AppException


class PhoneNumberIsAlreadyExists(AppException):
    code = 409
    message = 'Пользователь с таким телефоном уже существует'
