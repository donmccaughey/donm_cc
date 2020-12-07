from typing import Optional

from .node import Node, NodeType


class DocType(Node):
    def __init__(self, parent: Optional[Node]=None, **kwargs):
        super().__init__(
            name='doctype',
            parent=parent,
            node_type=NodeType.DOCTYPE,
            **kwargs,
        )

    def __str__(self) -> str:
        return self.tag()

    def tag(self) -> str:
        return '<!doctype html>'
