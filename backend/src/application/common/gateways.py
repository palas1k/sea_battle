from typing import Protocol


class UserGateway(Protocol):
    """
        Типизация для проверки корректности методов и свойств. Все классы наследуемые от UserGateway явно и не явно,
        должны переопределять указанные методы с указаными типами данных
    """
    async def get_by_username(self, username: str):
        ...

    async def create(self, username: str) -> None:
        ...

    async def update(self, username: str, new_username: str) -> None:
        ...

    async def delete(self, username: str) -> None:
        ...
