import asyncio
import os
from pathlib import Path

import structlog
import uvicorn
from dishka.integrations.aiogram import setup_dishka
from dishka.integrations.fastapi import DishkaApp

from src.config import Config, get_config
from src.infra.log import setup_logging
from src.main.di import DIProvider, UsecaseProvider
from src.main.socketio import setup_socketio
from src.main.telegram import setup_dispatcher
from src.main.web import setup_fastapi
from src.presentation.socketio.namespace import Namespace

logger = structlog.get_logger(__name__)


async def run() -> None:
    # поиск пути к ботку в env
    config_path = Path(os.getenv("CONFIG_PATH"))
    if not config_path.exists():
        raise RuntimeError("Config file does not exist")

    # получение конфига и передача логеру
    config: Config = get_config(config_path)
    setup_logging(config.logging)

    await logger.ainfo("Initializing aiogram")
    bot, dispatcher = await setup_dispatcher(config.telegram)
    # Di provider создание коннекта с psql и redis
    # UsecaseProvider хэндлить ответы от телеграма
    # и тут для чего dispatcher
    providers = [DIProvider(config, bot, dispatcher), UsecaseProvider()]

    # вызов методов создания коннекта с psql
    # для чего dispatcher?
    setup_dishka(providers, dispatcher)
    await logger.ainfo("Initializing fastapi")
    # запуск фастапи
    fastapi = setup_fastapi(config.api, config.telegram.token)
    await logger.ainfo("Starting service")
    # запуск socketio
    socketio = setup_socketio("/api/v1", fastapi)
    # хэндлер сокетайо видимо получать апдейты?1
    socketio.register_namespace(Namespace("/", providers))

    # запуск ювикорн видимо
    await uvicorn.Server(
        config=uvicorn.Config(app=DishkaApp(providers, fastapi), host=config.api.host, port=config.api.port,
                              workers=config.api.workers, )).serve()


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
