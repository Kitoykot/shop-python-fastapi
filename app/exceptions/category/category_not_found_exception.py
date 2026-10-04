from app.exceptions.app_exception import AppException


class CategoryNotFoundException(AppException):
    code = 404
    message = 'Категория не найдена'
