from app.exceptions.app_exception import AppException


class DeleteCartItemException(AppException):
    code = 409
    message = 'Нет возможности удалить товар из корзины. Попробуйте позже'
