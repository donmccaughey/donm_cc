from typing import Optional

from .node import Node, NodeType


class DocType(Node):
    def __init__(self, parent: Optional[Node]=None, **kwargs):
        super().__init__(
            name='doctype',
            parent=parent,
            type=NodeType.DOCTYPE,
            **kwargs,
        )

    def __str__(self):
        return '<!doctype html>'

    def write(self, f):
        f.write(str(self))
        f.write('\n')
