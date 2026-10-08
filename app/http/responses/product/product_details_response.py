from pydantic import BaseModel

from app.http.responses.types import Price


class ProductDetailsResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: Price
    is_available: bool
