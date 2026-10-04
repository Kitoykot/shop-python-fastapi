from decimal import Decimal

from pydantic import BaseModel


class ProductListResponse(BaseModel):
    id: int
    name: str
    price: Decimal
