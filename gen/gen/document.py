from .node import Node, NodeType


class Document(Node):
    def __init__(self, **kwargs):
        super().__init__(
            name='document',
            parent=None,
            node_type=NodeType.DOCUMENT,
            **kwargs,
        )

    def __str__(self) -> str:
        s = ''
        for child in self.children:
            s += str(child) + '\n'
        return s
