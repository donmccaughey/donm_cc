from .node import Node


class Document(Node):
    def __init__(self, **kwargs):
        super().__init__(
            name='document',
            parent=None,
            **kwargs,
        )

    def __str__(self) -> str:
        s = ''
        for child in self.children:
            s += str(child) + '\n'
        return s

    def attach(self, parent: Node):
        self.parent = None

    def markup(self, width: int) -> str:
        markup = ''
        for child in self.children:
            markup += child.markup(width)
        return markup
