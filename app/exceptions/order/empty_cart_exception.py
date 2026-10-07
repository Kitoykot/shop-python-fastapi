from app.exceptions.app_exception import AppException


class EmptyCartException(AppException):
    code = 400
    message = 'Чтобы сделать заказ - добавьте что-нибудь в корзину'
