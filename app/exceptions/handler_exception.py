
from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.app_exception import AppException


def app_exception_handler(_request: Request, exception: AppException):
    return JSONResponse(
        status_code=exception.code,
        content={
            "code": exception.code,
            "message": exception.message,
        },
    )
