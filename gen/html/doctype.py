from typing import Optional
from .node import Node
from .tag import Tag
from .tag_type import TagType


class DocType(Node):
    def __init__(self, parent: Optional[Node]=None, **kwargs):
        super().__init__(
            name='doctype',
            parent=parent,
            **kwargs,
        )

    def __str__(self) -> str:
        return self.tag()

    def tag(self) -> str:
        return '<!doctype html>'

    def tags(self) -> list[Tag]:
        return [
            Tag(
                name=self.name,
                text=self.tag(),
                type=TagType.DTD,
                format=self.format,
                omit=False,
                indent_children=False,
            )
        ]
