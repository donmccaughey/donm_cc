from dataclasses import dataclass
from enum import Enum, auto
from .format import Format


class TagType(Enum):
    DTD = auto()
    START = auto()
    END = auto()
    TEXT = auto()


@dataclass
class Tag:
    name: str
    text: str
    type: TagType
    format: Format
    has_end_tag: bool
    indent_children: bool
    is_heading: bool
    is_phrasing_content: bool

    @property
    def is_block(self) -> bool:
        return self.format == Format.BLOCK

    @property
    def is_compact(self) -> bool:
        return self.format == Format.COMPACT

    @property
    def is_dtd(self) -> bool:
        return self.type == TagType.DTD

    @property
    def is_end(self) -> bool:
        return self.type == TagType.END

    @property
    def is_inline(self) -> bool:
        return self.format == Format.INLINE

    @property
    def is_start(self) -> bool:
        return self.type == TagType.START

    @property
    def is_text(self) -> bool:
        return self.type == TagType.TEXT