from enum import unique, Enum, auto


@unique
class ElementType(Enum):
    CONTAINER = auto()
    COMPACT = auto()
    EMPTY = auto()