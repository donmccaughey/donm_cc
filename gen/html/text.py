import textwrap
from typing import Optional
from .node import Node
from .format import Format
from .tag import Tag, TagType


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

    def __str__(self) -> str:
        # TODO: HTML encode text
        return textwrap.fill(self.text.strip())

    def tags(self) -> list[Tag]:
        return [
            Tag(
                name='text',
                text=self.text,
                type=TagType.TEXT,
                format=self.format,
                has_end_tag=False,
                indent_children=False,
                is_heading=False,
                is_phrasing_content=False,
            )
        ]
