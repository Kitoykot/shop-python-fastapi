from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.db.db_dependency import get_db
from app.repositories.product.product_repository import ProductRepository
from app.services.product.product_service import ProductService


def get_product_service(session: Session = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(session))
