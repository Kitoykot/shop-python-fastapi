from app.exceptions.app_exception import AppException


class PaymentNotFoundException(AppException):
    message = 'Платеж не найден'
    code = 404
