from pydantic import BaseModel


class ProductDeletedResponse(BaseModel):
    message: str
