from enum import unique, Enum, auto


@unique
class Format(Enum):
    BLOCK = auto()
    COMPACT = auto()
    INLINE = auto()
