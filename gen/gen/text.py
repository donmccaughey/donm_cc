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
            type=NodeType.TEXT,
            **kwargs,
        )
        self.text = text

    def __str__(self):
        return self.text

    def write(self, f):
        f.write(self.text)
        f.write('\n')
