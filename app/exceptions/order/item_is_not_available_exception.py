from app.exceptions.app_exception import AppException


class ItemIsNotAvailableException(AppException):
    code = 409

    def __init__(self, product_name: str):
        self.message = f'Товар {product_name} в данный момент недоступен для заказа'

        super().__init__(self.message)
