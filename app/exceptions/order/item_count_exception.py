from app.exceptions.app_exception import AppException


class ItemCountException(AppException):
    code = 400

    def __init__(self, product_name: str):
        self.message = f'Товар {product_name} недоступен. Уменьшите количество товара в корзине'

        super().__init__(self.message)