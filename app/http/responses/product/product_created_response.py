
from pydantic import BaseModel


class ProductCreatedResponse(BaseModel):
    message: str
    code: int
