from pydantic import BaseModel


class CategoryCreatedResponse(BaseModel):
    code: int
    message: str
