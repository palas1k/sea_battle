from typing import Generic, TypeVar

InputDTO = TypeVar("InputDTO", covariant=True)
OutputDTO = TypeVar("OutputDTO", contravariant=True)


class Usecase(Generic[InputDTO, OutputDTO]):
    """
        Класс UseCase предполагает использование двух типов данных. Generic обощенный тип данных.
    """

    async def __call__(self, data: InputDTO) -> OutputDTO:
        pass
