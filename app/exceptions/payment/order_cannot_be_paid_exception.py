from app.exceptions.app_exception import AppException


class OrderCannotBePaidException(AppException):
    message = 'Оплатить можно только новый заказ'
    code = 409
