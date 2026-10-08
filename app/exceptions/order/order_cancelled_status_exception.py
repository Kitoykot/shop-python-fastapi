from app.exceptions.app_exception import AppException


class OrderCancelledStatusException(AppException):
    message = 'Заказ уже отменен'
    code = 409
