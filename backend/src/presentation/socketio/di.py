from dishka import make_async_container, Provider
from dishka.integrations.base import wrap_injection
from socketio import AsyncNamespace

SELF_PARAM = "self"


def inject(func):
    return wrap_injection(func, remove_depends=True, container_getter=lambda _, p: p["self"].dishka_container,
                          is_async=True)


class DishkaAsyncNamespace(AsyncNamespace):
    def __init__(self, namespace: str, providers: list[Provider]):
        self.container = make_async_container(*providers)
        super().__init__(namespace)

    async def __aenter__(self):
        await self.container.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.container.__aexit__(exc_type, exc_val, exc_tb)
