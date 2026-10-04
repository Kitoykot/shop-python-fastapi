from pydantic import BaseModel


class ProductUpdatedResponse(BaseModel):
    message: str
