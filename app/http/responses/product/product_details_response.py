from decimal import Decimal

from pydantic import BaseModel


class ProductDetailsResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: Decimal
    is_available: bool
