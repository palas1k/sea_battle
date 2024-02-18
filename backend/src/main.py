import asyncio
import os
from pathlib import Path
from typing import AsyncIterable

import structlog
import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from dishka import provide, Provider, Scope
from dishka.integrations.aiogram import setup_dishka
from dishka.integrations.fastapi import DishkaApp
from fastapi import FastAPI
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from starlette.middleware.cors import CORSMiddleware

from src.application.handle_update import HandleUpdate
from src.config import ApiConfig, Config, get_config, StorageType, TelegramConfig
from src.infra.log import setup_logging
from src.presentation.fastapi.setup import setup_routes

logger = structlog.get_logger(__name__)


class DIProvider(Provider):
    def __init__(self, config: Config, bot: Bot, dispatcher: Dispatcher):
        self.config = config
        self.bot = bot
        self.dispatcher = dispatcher
        super().__init__()

    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncIterable[AsyncEngine]:
        engine: AsyncEngine = create_async_engine(self.config.database.dsn)
        yield engine

        await engine.dispose()

    @provide(scope=Scope.APP)
    async def get_session_maker(
        self, engine: AsyncEngine
    ) -> AsyncIterable[async_sessionmaker]:
        yield async_sessionmaker(engine, autoflush=False, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    async def get_redis(self) -> AsyncIterable[Redis]:
        yield Redis.from_url(self.config.redis.url)


class UsecaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_dispatch_update(
        self, bot: Bot, dp: Dispatcher
    ) -> AsyncIterable[HandleUpdate]:
        yield HandleUpdate(bot=bot, dp=dp)


async def setup_dispatcher(config: TelegramConfig) -> tuple[Bot, Dispatcher]:
    storage = MemoryStorage()
    if config.storage == StorageType.redis:
        redis = Redis(**config.storage_args)
        storage = RedisStorage(redis)

    dp = Dispatcher(storage=storage)
    # dp.include_router(router)

    bot = Bot(config.token)

    await bot.delete_webhook(drop_pending_updates=True)
    if await bot.set_webhook(f"{config.webhook_base}/api/{bot.token}"):
        await logger.ainfo(
            "Bot started on hook: %s", f"{config.webhook_base}/api/{bot.token}"
        )

    return bot, dp


def setup_fastapi(config: ApiConfig, token: str) -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=config.allow_credentials,
        allow_methods=config.allow_methods,
        allow_headers=config.allow_headers,
    )

    setup_routes(app, token)

    return app


async def run() -> None:
    config_path = Path(os.getenv("CONFIG_PATH"))
    if not config_path.exists():
        raise RuntimeError("Config file does not exist")

    config: Config = get_config(config_path)
    setup_logging(config.logging)

    await logger.ainfo("Initializing aiogram")
    bot, dispatcher = await setup_dispatcher(config.telegram)
    providers = [DIProvider(config, bot, dispatcher), UsecaseProvider()]

    setup_dishka(providers, dispatcher)
    await logger.ainfo("Initializing fastapi")
    fastapi = setup_fastapi(config.api, config.telegram.token)
    await logger.ainfo("Starting service")

    server = uvicorn.Server(
        config=uvicorn.Config(
            app=DishkaApp(providers, fastapi),
            host=config.api.host,
            port=config.api.port,
            workers=config.api.workers,
        )
    )
    await server.serve()


def main() -> None:
    try:
        asyncio.run(run())
        exit(os.EX_OK)
    except SystemExit:
        exit(os.EX_OK)
    except BaseException:
        logger.exception("Unexpected error occurred")
        exit(os.EX_SOFTWARE)


if __name__ == "__main__":
    main()
