from app.exceptions.app_exception import AppException


class OrderCompletedStatusException(AppException):
    message = 'Нельзя отменить заказ: он уже завершен'
    code = 409
