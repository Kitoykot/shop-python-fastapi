from pydantic import BaseModel


class CategoryUpdatedResponse(BaseModel):
    code: int
    message: str
