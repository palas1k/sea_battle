from typing import Protocol


class UserGateway(Protocol):
    async def get_by_username(self, username: str):
        ...

    async def create(self, username: str) -> None:
        ...

    async def update(self, username: str, new_username: str) -> None:
        ...

    async def delete(self, username: str) -> None:
        ...
