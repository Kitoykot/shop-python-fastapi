from pydantic import BaseModel, Field

from app.dto.cart.update_cart_item_dto import UpdateCartItemDto


class UpdateCartItemRequest(BaseModel):
    product_id: int = Field(gt=0)
    count: int = Field(gt=0, le=32767)

    def to_dto(self) -> UpdateCartItemDto:
        return UpdateCartItemDto(
            product_id=self.product_id,
            count=self.count,
        )
