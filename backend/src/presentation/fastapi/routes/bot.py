from typing import Annotated

from dishka.integrations.base import Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request

from src.application.handle_update import HandleUpdate, HandleUpdateDTO

router = APIRouter()


@inject
async def handle_update(
    update: dict,
    request: Request,
    dispatch_update_usecase: Annotated[HandleUpdate, Depends()],
):
    await dispatch_update_usecase(
        HandleUpdateDTO(raw_update=update, container=request.state.dishka_container)
    )
