from app.exceptions.app_exception import AppException


class PaymentCannotBeConfirmedException(AppException):
    message = 'Этот платеж нельзя подтвердить'
    code = 409
