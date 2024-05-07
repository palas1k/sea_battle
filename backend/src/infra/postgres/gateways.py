import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.gateways import UserGateway
from src.infra.postgres.models import UserModel

logger = structlog.get_logger(__name__)


class SAGateway:
    def __init__(self, session: AsyncSession):
        self.session = session


class SAUserGateway(SAGateway, UserGateway):
    """
     Методы запросов к бд наследуемые для типизации от  Сессия и UserGateway с типизацией методов.
     Класс реализует CRUD запросов к бд
    """
    async def get_by_username(self, username: str):
        return (
            await self.session.execute(
                select(UserModel).where(UserModel.username == username)
            )
        ).one_or_none()

    async def create(self, username: str) -> None:
        model = UserModel(username=username)

        try:
            self.session.add(model)
            await self.session.flush()
        except Exception as e:
            await logger.aerror("SA Exception", e)

    async def update(self, username: str, new_username: str) -> None:
        await self.session.execute(
            update(UserModel)
            .where(UserModel.username == username)
            .values(username=new_username)
        )

    async def delete(self, username: str) -> None:
        model = self.session.get(UserModel, username)
        if model is None:
            return

        await self.session.delete(model)
