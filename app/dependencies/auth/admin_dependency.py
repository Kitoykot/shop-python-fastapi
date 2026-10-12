from fastapi import Depends

from app.dependencies.auth.current_user_dependency import get_current_user
from app.dto.user.read.data.user_data_dto import UserDataDto
from app.enums.user.user_role import UserRole
from app.exceptions.auth.forbidden_exception import ForbiddenException


def get_admin(user: UserDataDto = Depends(get_current_user)) -> UserDataDto:
    if user.role != UserRole.ADMIN:
        raise ForbiddenException()

    return user
