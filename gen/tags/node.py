from __future__ import annotations

from enum import Enum, unique, auto
from typing import Optional


with_node: list[Optional[Node]] = [None]


@unique
class NodeType(Enum):
    DOCTYPE = auto()
    DOCUMENT = auto()
    ELEMENT = auto()
    TEXT = auto()


class Node:
    def __init__(
            self,
            name: str,
            node_type: NodeType,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.children: list[Node] = []
        self.name = name
        self.node_type = node_type
        if self.node_type == NodeType.DOCUMENT:
            self.parent = None
        else:
            self.attach(parent if parent else with_node[-1])

    def __enter__(self):
        with_node.append(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        with_node.pop()

    @property
    def has_children(self) -> bool:
        return len(self.children) > 0

    @property
    def rank(self) -> int:
        return self.parent.rank + 1 if self.parent else 0

    def __str__(self) -> str:
        raise NotImplementedError

    def attach(self, parent: Node):
        self.parent = parent
        parent.children.append(self)

    def attach_children(self, children: list[Node]):
        for child in children:
            child.attach(self)

    def detach(self):
        if self.parent:
            self.parent.children.remove(self)
            self.parent = None

    def detach_children(self) -> list[Node]:
        children = list(self.children)
        for child in children:
            child.detach()
        assert not self.children
        return children
