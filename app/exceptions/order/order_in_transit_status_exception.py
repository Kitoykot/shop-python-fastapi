from app.exceptions.app_exception import AppException


class OrderInTransitStatusException(AppException):
    message = 'Нельзя отменить заказ: он уже в пути'
    code = 409
