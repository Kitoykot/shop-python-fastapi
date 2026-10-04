from fastapi import APIRouter, Depends, status

from app.dependencies.product.product_dependencies import get_product_service
from app.http.requests.product.create_product_request import CreateProductRequest
from app.http.requests.product.update_product_request import UpdateProductRequest
from app.http.responses.product.product_created_response import ProductCreatedResponse
from app.http.responses.product.product_deleted_response import ProductDeletedResponse
from app.http.responses.product.product_details_response import ProductDetailsResponse
from app.http.responses.product.product_list_response import ProductListResponse
from app.http.responses.product.product_updated_response import ProductUpdatedResponse
from app.services.product.product_service import ProductService

router = APIRouter(prefix='/products')


@router.get('')
def products_list(
    service: ProductService = Depends(get_product_service),
) -> list[ProductListResponse]:
    products = service.get_active_products()

    return [
        ProductListResponse.model_validate(product, from_attributes=True)
        for product in products
    ]


@router.get('/{id}')
def product_by_id(
    id: int, service: ProductService = Depends(get_product_service)
) -> ProductDetailsResponse:
    product = service.get_product_details(id)
    return ProductDetailsResponse.model_validate(product, from_attributes=True)


@router.post('', status_code=status.HTTP_201_CREATED)
def create(
    request: CreateProductRequest,
    service: ProductService = Depends(get_product_service),
) -> ProductCreatedResponse:
    service.create_product(request.create_dto())

    return ProductCreatedResponse(
        message='Товар создан',
        code=status.HTTP_201_CREATED,
    )


@router.patch('/{id}')
def update(
    id: int,
    request: UpdateProductRequest,
    service: ProductService = Depends(get_product_service),
) -> ProductUpdatedResponse:
    service.update_product(id, request.create_dto())

    return ProductUpdatedResponse(message='Товар обновлен')


@router.delete('/{id}')
def delete(
    id: int, service: ProductService = Depends(get_product_service)
) -> ProductDeletedResponse:
    service.delete_product(id)

    return ProductDeletedResponse(message='Товар удален')
