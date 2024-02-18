from dataclasses import dataclass


@dataclass
class Cell:
    pass


FieldCells = tuple[
    tuple[Cell, Cell, Cell, Cell, Cell],
    tuple[Cell, Cell, Cell, Cell, Cell],
    tuple[Cell, Cell, Cell, Cell, Cell],
    tuple[Cell, Cell, Cell, Cell, Cell],
    tuple[Cell, Cell, Cell, Cell, Cell],
]


@dataclass
class Field:
    cells: FieldCells


@dataclass
class SessionState:
    pass


@dataclass
class ActiveSession:
    pass
