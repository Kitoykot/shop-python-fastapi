from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
