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
        elif parent:
            self.parent = parent
        else:
            self.parent = with_node[-1]
        if self.parent:
            self.parent.children.append(self)

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

    def detach(self):
        if self.parent:
            self.parent.children.remove(self)
