from .node import Node, NodeType


class Document(Node):
    def __init__(self, **kwargs):
        super().__init__(
            name='document',
            parent=None,
            type=NodeType.DOCUMENT,
            **kwargs,
        )

    def __str__(self):
        return '(document)'

    def write(self, f):
        for child in self.children:
            child.write(f)
