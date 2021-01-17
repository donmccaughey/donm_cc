from dataclasses import dataclass

from .tag_type import TagType
from .format import Format


@dataclass
class Tag:
    name: str
    text: str
    type: TagType
    format: Format
    omit: bool
    indent_children: bool
