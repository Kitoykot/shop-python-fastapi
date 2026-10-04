from pydantic import BaseModel, Field

from app.dto.category.update_category_dto import UpdateCategoryDto


class UpdateCategoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=256)

    def create_dto(self) -> UpdateCategoryDto:
        return UpdateCategoryDto(name=self.name)
