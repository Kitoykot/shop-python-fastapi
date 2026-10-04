from pydantic import BaseModel


class ProductAttachedResponse(BaseModel):
    code: int
    message: str
