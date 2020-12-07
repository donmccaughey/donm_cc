from __future__ import annotations

from enum import Enum, unique
from typing import Optional


_with_node: list[Optional[Node]] = [None]


@unique
class NodeType(Enum):
    ELEMENT = 1
    TEXT = 3
    DOCUMENT = 9
    DOCTYPE = 10


class Node:
    def __init__(self, name: str, type: NodeType, parent: Optional[Node]=None, **kwargs):
        super().__init__(**kwargs)
        self.children: list[Node] = []
        self.name = name
        self.parent = parent if parent else _with_node[-1]
        self.type = type
        if self.parent:
            self.parent.children.append(self)

    def __enter__(self):
        global _with_node
        _with_node.append(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        _with_node.pop()

    @property
    def has_children(self) -> bool:
        return len(self.children) > 0

    @property
    def rank(self) -> int:
        return self.parent.rank + 1 if self.parent else 0

    def __str__(self):
        raise NotImplementedError

    def write(self, f):
        raise NotImplementedError
