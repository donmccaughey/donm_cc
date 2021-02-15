from typing import Optional
from .node import Node


class DocType(Node):
    def __init__(self, parent: Optional[Node]=None, **kwargs):
        super().__init__(
            name='doctype',
            parent=parent,
            **kwargs,
        )

    def markup(self, width: int) -> str:
        return '<!doctype html>\n'

    def tag(self) -> str:
        return '<!doctype html>'
