from pydantic import BaseModel


class OrderStatusResponse(BaseModel):
    code: str
    label: str
