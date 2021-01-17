import textwrap
from typing import Optional
from .node import Node
from .format import Format
from .tag import Tag
from .tag_type import TagType


class Text(Node):
    def __init__(
            self,
            text: str,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name='text',
            parent=parent,
            **kwargs,
        )
        self.format = Format.INLINE
        self.text = text

    def tags(self) -> list[Tag]:
        return [
            Tag(
                name='text',
                text=self.text,
                type=TagType.TEXT,
                format=self.format,
                omit=False,
                indent_children=False,
            )
        ]
