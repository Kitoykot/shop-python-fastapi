from app.exceptions.app_exception import AppException


class OrderNotFoundException(AppException):
    message = 'Заказ не найден'
    code = 404
