from fastapi import FastAPI
from starlette import status

from src.presentation.fastapi.exception_handlers import setup_exception_handlers
from src.presentation.fastapi.routes.bot import handle_update


def setup_routes(app: FastAPI, token: str) -> None:
    app.post(f"/api/{token}", status_code=status.HTTP_200_OK, include_in_schema=False)(
        handle_update
    )
    setup_exception_handlers(app)
