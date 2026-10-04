from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.db.db_dependency import get_db
from app.repositories.category.category_repository import CategoryRepository
from app.repositories.product.product_repository import ProductRepository
from app.services.category.category_service import CategoryService


def get_category_service(session: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(
        repository=CategoryRepository(session),
        product_repository=ProductRepository(session),
    )
