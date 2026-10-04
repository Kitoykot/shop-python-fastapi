from app.exceptions.app_exception import AppException


class ProductNotFoundException(AppException):
    code = 404
    message = "Товар не найден или недоступен"
