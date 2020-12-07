from typing import Optional

from .node import Node, NodeType


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
            node_type=NodeType.TEXT,
            **kwargs,
        )
        self.text = text

    def __str__(self) -> str:
        return self.text
