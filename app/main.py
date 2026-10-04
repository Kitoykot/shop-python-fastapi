from fastapi import FastAPI

from app.exceptions.app_exception import AppException
from app.exceptions.handler_exception import app_exception_handler
from app.http.controllers.api.v1.router import router as router_v1

app = FastAPI()

app.include_router(router_v1)
app.add_exception_handler(AppException, app_exception_handler)
