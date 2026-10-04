from decimal import Decimal

from pydantic import BaseModel, Field

from app.dto.product.update_product_dto import UpdateProductDto


class UpdateProductRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=256)
    description: str | None = None
    price: Decimal | None = Field(default=None, ge=0)
    show_in_catalog: bool | None = None
    count: int | None = Field(default=None, ge=0, le=32767)

    def create_dto(self) -> UpdateProductDto:
        return UpdateProductDto(fields=self.model_dump(exclude_unset=True))
