from sqlalchemy import Column, ForeignKey, Integer, Table

from app.models.base import Base

category_products = Table(
    'category_products',
    Base.metadata,
    Column(
        'category_id',
        Integer,
        ForeignKey('categories.id', ondelete='CASCADE'),
        primary_key=True,
    ),
    Column(
        'product_id',
        Integer,
        ForeignKey('products.id', ondelete='CASCADE'),
        primary_key=True,
    ),
)
