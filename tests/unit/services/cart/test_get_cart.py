from decimal import Decimal
from unittest.mock import Mock

from app.dto.cart.cart_item_dto import CartItemDto
from app.dto.cart.data.cart_data_dto import CartDataDto
from app.dto.cart.data.cart_item_data_dto import CartItemDataDto
from app.dto.product.product_dto import ProductDto
from app.repositories.cart.cart_repository import CartRepository
from app.repositories.product.product_repository import ProductRepository
from app.services.cart.cart_service import CartService

class TestGetCart:
    def setup_method(self):
        self.cart_repository = Mock(spec=CartRepository)
        self.product_repository = Mock(spec=ProductRepository)

        self.service = CartService(
            repository=self.cart_repository,
            product_repository=self.product_repository
        )


    def test_missing_cart(self) -> None:
        self.cart_repository.get_cart_details.return_value = None
        result = self.service.get_cart(user_id=1)
        
        assert result.cart.items_count == 0
        assert result.cart.total_price == Decimal('0')
        assert result.items == []


    def test_empty_cart(self) -> None:
        self.cart_repository.get_cart_details.return_value = CartDataDto(
            id=1,
            user_id=1,
            items=[]
        )
        result = self.service.get_cart(user_id=1)

        assert result.cart.items_count == 0
        assert result.cart.total_price == Decimal('0')
        assert result.items == []


    def test_available_items(self) -> None:
        self.cart_repository.get_cart_details.return_value = CartDataDto(
            id=1,
            user_id=1,
            items=[
                CartItemDataDto(
                    id=1,
                    count=2,
                    product=ProductDto(
                        id=2,
                        name='Product 1',
                        description='',
                        price=Decimal('10.50'),
                        show_in_catalog=True,
                        count=10,
                        is_available=True,
                    ),
                ),
                CartItemDataDto(
                    id=3,
                    count=4,
                    product=ProductDto(
                        id=4,
                        name='Product 2',
                        description='',
                        price=Decimal('20.50'),
                        show_in_catalog=True,
                        count=20,
                        is_available=True,
                    ),
                ),
            ],
        )
        result = self.service.get_cart(user_id=1)
        self.cart_repository.get_cart_details.assert_called_once_with(1)

        assert result.cart.items_count == 6
        assert result.cart.total_price == Decimal('103')
        assert result.items == [
            CartItemDto(
                id=1,
                product_id=2,
                name='Product 1',
                count=2,
                price=Decimal('10.50'),
                is_available=True,
            ),
            CartItemDto(
                id=3,
                product_id=4,
                name='Product 2',
                count=4,
                price=Decimal('20.50'),
                is_available=True,
            ),
        ]

    
    def test_unavailable_product(self) -> None:
        self.cart_repository.get_cart_details.return_value = CartDataDto(
            id=1,
            user_id=1,
            items=[
                CartItemDataDto(
                    id=1,
                    count=2,
                    product=ProductDto(
                        id=1,
                        name='Product 1',
                        description='',
                        price=Decimal('10.50'),
                        show_in_catalog=True,
                        count=10,
                        is_available=True,
                    ),
                ),
                CartItemDataDto(
                    id=2,
                    count=4,
                    product=ProductDto(
                        id=2,
                        name='Product 2',
                        description='',
                        price=Decimal('20.50'),
                        show_in_catalog=False,
                        count=20,
                        is_available=False,
                    ),
                ),
            ],
        )
        result = self.service.get_cart(user_id=1)

        assert result.cart.items_count == 2
        assert result.cart.total_price == Decimal('21')
        assert result.items == [
            CartItemDto(
                id=1,
                product_id=1,
                name='Product 1',
                count=2,
                price=Decimal('10.50'),
                is_available=True,
            ),
            CartItemDto(
                id=2,
                product_id=2,
                name='Product 2',
                count=4,
                price=Decimal('20.50'),
                is_available=False,
            ),
        ]


    def test_insufficient_stock(self) -> None:
        self.cart_repository.get_cart_details.return_value = CartDataDto(
            id=1,
            user_id=1,
            items=[
                CartItemDataDto(
                    id=1,
                    count=2,
                    product=ProductDto(
                        id=1,
                        name='Product 1',
                        description='',
                        price=Decimal('10.50'),
                        show_in_catalog=True,
                        count=10,
                        is_available=True,
                    ),
                ),
                CartItemDataDto(
                    id=2,
                    count=4,
                    product=ProductDto(
                        id=2,
                        name='Product 2',
                        description='',
                        price=Decimal('20.50'),
                        show_in_catalog=True,
                        count=2,
                        is_available=True,
                    ),
                ),
            ],
        )
        result = self.service.get_cart(user_id=1)

        assert result.cart.items_count == 2
        assert result.cart.total_price == Decimal('21')
        assert result.items == [
            CartItemDto(
                id=1,
                product_id=1,
                name='Product 1',
                count=2,
                price=Decimal('10.50'),
                is_available=True,
            ),
            CartItemDto(
                id=2,
                product_id=2,
                name='Product 2',
                count=4,
                price=Decimal('20.50'),
                is_available=False,
            ),
        ]


    def test_stock_is_none(self) -> None:
        self.cart_repository.get_cart_details.return_value = CartDataDto(
            id=1,
            user_id=1,
            items=[
                CartItemDataDto(
                    id=1,
                    count=2,
                    product=ProductDto(
                        id=1,
                        name='Product 1',
                        description='',
                        price=Decimal('10.50'),
                        show_in_catalog=True,
                        count=10,
                        is_available=True,
                    ),
                ),
                CartItemDataDto(
                    id=2,
                    count=4,
                    product=ProductDto(
                        id=2,
                        name='Product 2',
                        description='',
                        price=Decimal('20.50'),
                        show_in_catalog=True,
                        count=None,
                        is_available=False,
                    ),
                ),
            ],
        )
        result = self.service.get_cart(user_id=1)

        assert result.cart.items_count == 2
        assert result.cart.total_price == Decimal('21')
        assert result.items == [
            CartItemDto(
                id=1,
                product_id=1,
                name='Product 1',
                count=2,
                price=Decimal('10.50'),
                is_available=True,
            ),
            CartItemDto(
                id=2,
                product_id=2,
                name='Product 2',
                count=4,
                price=Decimal('20.50'),
                is_available=False,
            ),
        ]


    def test_stock_equals_quantity(self) -> None:
        self.cart_repository.get_cart_details.return_value = CartDataDto(
            id=1,
            user_id=1,
            items=[
                CartItemDataDto(
                    id=1,
                    count=2,
                    product=ProductDto(
                        id=1,
                        name='Product 1',
                        description='',
                        price=Decimal('10.50'),
                        show_in_catalog=True,
                        count=2,
                        is_available=True,
                    ),
                ),
                CartItemDataDto(
                    id=2,
                    count=4,
                    product=ProductDto(
                        id=2,
                        name='Product 2',
                        description='',
                        price=Decimal('20.50'),
                        show_in_catalog=True,
                        count=4,
                        is_available=True,
                    ),
                ),
            ],
        )
        result = self.service.get_cart(user_id=1)

        assert result.cart.items_count == 6
        assert result.cart.total_price == Decimal('103')
        assert result.items == [
            CartItemDto(
                id=1,
                product_id=1,
                name='Product 1',
                count=2,
                price=Decimal('10.50'),
                is_available=True,
            ),
            CartItemDto(
                id=2,
                product_id=2,
                name='Product 2',
                count=4,
                price=Decimal('20.50'),
                is_available=True,
            ),
        ]


    def test_all_items_unavailable(self) -> None:
        self.cart_repository.get_cart_details.return_value = CartDataDto(
            id=1,
            user_id=1,
            items=[
                CartItemDataDto(
                    id=1,
                    count=2,
                    product=ProductDto(
                        id=1,
                        name='Product 1',
                        description='',
                        price=Decimal('10.50'),
                        show_in_catalog=True,
                        count=0,
                        is_available=False,
                    ),
                ),
                CartItemDataDto(
                    id=2,
                    count=4,
                    product=ProductDto(
                        id=2,
                        name='Product 2',
                        description='',
                        price=Decimal('20.50'),
                        show_in_catalog=True,
                        count=3,
                        is_available=True,
                    ),
                ),
            ],
        )
        result = self.service.get_cart(user_id=1)

        assert result.cart.items_count == 0
        assert result.cart.total_price == Decimal('0')
        assert result.items == [
            CartItemDto(
                id=1,
                product_id=1,
                name='Product 1',
                count=2,
                price=Decimal('10.50'),
                is_available=False,
            ),
            CartItemDto(
                id=2,
                product_id=2,
                name='Product 2',
                count=4,
                price=Decimal('20.50'),
                is_available=False,
            ),
        ]