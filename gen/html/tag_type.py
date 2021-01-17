from enum import Enum, auto


class TagType(Enum):
    COMMENT = auto()
    DTD = auto()
    START = auto()
    END = auto()
    TEXT = auto()