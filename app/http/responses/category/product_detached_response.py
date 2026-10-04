from pydantic import BaseModel


class ProductDetachedResponse(BaseModel):
    code: int
    message: str
