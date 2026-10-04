from pydantic import BaseModel, Field

from app.dto.category.create_category_dto import CreateCategoryDto


class CreateCategoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=256)

    def create_dto(self) -> CreateCategoryDto:
        return CreateCategoryDto(name=self.name)
