from pydantic import BaseModel


class CategoryDeletedResponse(BaseModel):
    code: int
    message: str
