from dataclasses import dataclass

from aiogram import Bot, Dispatcher
from dishka import AsyncContainer

from src.application.common.usecase import Usecase


@dataclass(slots=True)
class HandleUpdateDTO:
    raw_update: dict
    container: AsyncContainer


class HandleUpdate(Usecase[HandleUpdateDTO, None]):
    """
     "Отлов" апдейтов от телеграм, дочерний класс от Usecase с типами Input, Output DTO
    """
    __slots__ = ("bot", "dp")

    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp

    async def __call__(self, data: HandleUpdateDTO) -> None:
        await self.dp.feed_raw_update(
            self.bot, data.raw_update, container=data.container
        )
