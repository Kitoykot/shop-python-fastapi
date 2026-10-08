from pydantic import BaseModel


class PaginationResponse(BaseModel):
    page: int
    per_page: int
    total: int
    pages: int
