from fastapi import APIRouter, Depends, status

from app.dependencies.category.category_dependencies import get_category_service

from app.http.requests.category.create_category_request import CreateCategoryRequest
from app.http.requests.category.update_category_request import UpdateCategoryRequest
from app.http.responses.category.category_response import CategoryResponse
from app.http.responses.category.category_created_response import CategoryCreatedResponse
from app.http.responses.category.category_details_response import CategoryDetailsResponse
from app.http.responses.category.category_deleted_response import CategoryDeletedResponse
from app.http.responses.category.category_updated_response import CategoryUpdatedResponse
from app.http.responses.category.product_attached_response import ProductAttachedResponse
from app.http.responses.category.product_detached_response import ProductDetachedResponse

from app.services.category.category_service import CategoryService

router = APIRouter(prefix="/categories")


@router.get("", response_model=list[CategoryResponse])
def categories_list(service: CategoryService = Depends(get_category_service)) -> list[CategoryResponse]:
    categories = service.get_active_categories()

    return [
        CategoryResponse.model_validate(category, from_attributes=True)
        for category in categories
    ]


@router.get("/{id}")
def category_by_id(id: int, service: CategoryService = Depends(get_category_service)) -> CategoryDetailsResponse:
    details = service.get_category_details(id)

    return CategoryDetailsResponse.model_validate(details, from_attributes=True)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CategoryCreatedResponse)
def create(request: CreateCategoryRequest, service: CategoryService = Depends(get_category_service)) -> CategoryCreatedResponse:
    service.create_category(request.create_dto())

    return CategoryCreatedResponse(
        code=status.HTTP_201_CREATED,
        message="Категория создана",
    )


@router.patch("/{id}")
def update_category(id: int, request: UpdateCategoryRequest, service: CategoryService = Depends(get_category_service)) -> CategoryUpdatedResponse:
    service.update_category(id, request.create_dto())

    return CategoryUpdatedResponse(
        code=status.HTTP_200_OK,
        message="Категория обновлена",
    )


@router.delete("/{id}")
def delete_category(id: int, service: CategoryService = Depends(get_category_service)) -> CategoryDeletedResponse:
    service.delete_category(id)

    return CategoryDeletedResponse(
        code=status.HTTP_200_OK,
        message="Категория удалена",
    )


@router.put( "/{id}/products/{product_id}", status_code=status.HTTP_201_CREATED)
def attach_product(id: int, product_id: int, service: CategoryService = Depends(get_category_service)) -> ProductAttachedResponse:
    service.attach_product(category_id=id, product_id=product_id)

    return ProductAttachedResponse(
        code=status.HTTP_201_CREATED,
        message="Товар прикреплен",
    )


@router.delete("/{id}/products/{product_id}", response_model=ProductDetachedResponse)
def detach_product(id: int, product_id: int, service: CategoryService = Depends(get_category_service)) -> ProductDetachedResponse:
    service.detach_product(category_id=id, product_id=product_id)

    return ProductDetachedResponse(
        code=status.HTTP_200_OK,
        message="Товар откреплен",
    )
