from sqlalchemy import select, delete
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.dialects.postgresql import insert

from app.dto.cart.data.cart_data_dto import CartDataDto
from app.dto.cart.data.cart_item_data_dto import CartItemDataDto
from app.dto.cart.update_cart_item_dto import UpdateCartItemDto

from app.dto.product.product_dto import ProductDto
from app.models.cart.cart import Cart
from app.models.cart.cart_item import CartItem
from app.models.product.product import Product



class CartRepository:
    def __init__(self, session: Session):
        self.session = session


    def get_cart_details(self, user_id: int) -> CartDataDto | None:
        statement = (
            select(Cart)
            .where(Cart.user_id == user_id)
            .options(
                selectinload(Cart.items)
                .selectinload(CartItem.product)
            )
        )

        cart = self.session.scalar(statement)
        
        if cart is None:
            return None

        return self.__to_dto(cart)
    

    def update_cart_item(self, user_id: int, dto: UpdateCartItemDto) -> None:
        cart = self.__get_or_create_cart(user_id)

        statement = (
            insert(CartItem)
            .values(
                cart_id=cart.id,
                product_id=dto.product_id,
                count=dto.count,
            )
            .on_conflict_do_update(
                index_elements=['cart_id', 'product_id'],
                set_={'count': dto.count}
            )
        )

        self.session.execute(statement)
        self.session.commit()


    def delete_cart_item(self, item_id: int, user_id: int) -> None:
        cart_id = self.__get_cart_id_or_none(user_id)

        if cart_id is None:
            return

        statement = (
            delete(CartItem)
            .where(
                CartItem.id == item_id,
                CartItem.cart_id == cart_id
            )
        )
        self.session.execute(statement)
        self.session.commit()


    def delete_all_cart_items(self, user_id: int) -> None:
        cart_id = self.__get_cart_id_or_none(user_id)

        if cart_id is None:
            return

        statement = (
            delete(CartItem)
            .where(CartItem.cart_id == cart_id)
        )
        self.session.execute(statement)
        self.session.commit()


    def __to_dto(self, cart: Cart) -> CartDataDto:
        return CartDataDto(
            id=cart.id,
            user_id=cart.user_id,
            items=[
                CartItemDataDto(
                    id=item.id,
                    count=item.count,
                    product=self.__to_product_dto(item.product),
                )
                for item in cart.items
            ],
        )


    def __to_product_dto(self, product: Product) -> ProductDto:
        return ProductDto(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                show_in_catalog=product.show_in_catalog,
                count=product.count,
                is_available=product.is_available,
            )


    def __get_or_create_cart(self, user_id: int) -> Cart:
        statement = (
            insert(Cart)
            .values(user_id=user_id)
            .on_conflict_do_nothing(index_elements=['user_id'])
            .returning(Cart)
        )

        cart = self.session.scalar(statement)

        if cart is not None:
            return cart

        existing_cart_statement = select(Cart).where(Cart.user_id == user_id)
        return self.session.execute(existing_cart_statement).scalar_one()


    def __get_cart_id_or_none(self, user_id: int) -> int | None:
        statement = (
            select(Cart.id)
            .where(Cart.user_id == user_id)
        )

        return self.session.scalar(statement)
