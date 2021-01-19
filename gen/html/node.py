from __future__ import annotations
from typing import Optional
from html.format import Format
from html.tag import Tag


with_node: list[Optional[Node]] = [None]


class Node:
    def __init__(
            self,
            name: str,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.children: list[Node] = []
        self.format = Format.BLOCK
        self.name = name
        self.next_sibling: Optional[Node] = None
        self.parent = None
        self.previous_sibling: Optional[Node] = None
        if not parent:
            parent = with_node[-1]
        if parent:
            self.attach(parent)

    def __enter__(self):
        with_node.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with_node.pop()

    @property
    def has_children(self) -> bool:
        return len(self.children) > 0

    def attach(self, parent: Node):
        self.parent = parent
        self.previous_sibling = (
            self.parent.children[-1] if self.parent.children else None
        )
        if self.previous_sibling:
            self.previous_sibling.next_sibling = self
        self.parent.children.append(self)

    def attach_children(self, children: list[Node]):
        for child in children:
            child.attach(self)

    def detach(self):
        if self.parent:
            self.parent.children.remove(self)
            self.parent = None
            if self.previous_sibling:
                self.previous_sibling.next_sibling = self.next_sibling
                self.previous_sibling = None
            self.next_sibling = None

    def detach_children(self) -> list[Node]:
        children = list(self.children)
        for child in children:
            child.detach()
        assert not self.children
        return children

    def markup(self, width: int) -> str:
        raise NotImplementedError

    def tokens(self) -> list[str]:
        raise NotImplementedError

    def tags(self) -> list[Tag]:
        raise NotImplementedError
