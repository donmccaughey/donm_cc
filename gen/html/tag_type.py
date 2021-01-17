from enum import Enum, auto


class TagType(Enum):
    DTD = auto()
    START = auto()
    END = auto()
    TEXT = auto()