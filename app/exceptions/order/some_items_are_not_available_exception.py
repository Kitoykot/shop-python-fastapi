from app.exceptions.app_exception import AppException


class SomeItemsAreNotAvailableException(AppException):
    code = 400
    message = 'Некоторые товары недоступны для заказа. Проверьте корзину и удалите недоступные товары'