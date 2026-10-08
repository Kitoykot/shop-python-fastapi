from decimal import Decimal

from pydantic import BaseModel, Field

from app.dto.product.create.create_product_dto import CreateProductDto


class CreateProductRequest(BaseModel):
    name: str = Field(min_length=1, max_length=256)
    description: str | None = None
    price: Decimal = Field(ge=0)
    show_in_catalog: bool = False
    count: int = Field(default=0, ge=0, le=32767)

    def create_dto(self) -> CreateProductDto:
        return CreateProductDto(
            name=self.name,
            description=self.description,
            price=self.price,
            show_in_catalog=self.show_in_catalog,
            count=self.count,
        )
