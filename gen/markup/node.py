from __future__ import annotations
from typing import Optional, Callable

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

    def __iter__(self):
        yield self
        for child in self.children:
            yield from child

    @property
    def has_children(self) -> bool:
        return len(self.children) > 0

    def accumulate_nodes(self, nodes: list):
        nodes.append(self)
        for child in self.children:
            child.accumulate_nodes(nodes)

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
        return self.detach_descendants(lambda node: True)

    def detach_descendants(self, matching: Callable[[Node], bool]) -> list[Node]:
        detached = []
        for child in list(self.children):
            if matching(child):
                child.detach()
                detached.append(child)
            else:
                detached += child.detach_descendants(matching)
        return detached

    def insert_after(self, node: Node):
        node.parent = self.parent
        node.previous_sibling = self
        node.next_sibling = self.next_sibling

        if self.next_sibling:
            self.next_sibling.previous_sibling = node
        self.next_sibling = node

        i = self.parent.children.index(self)
        self.parent.children.insert(i + 1, node)

    def markup(self, width: int) -> str:
        raise NotImplementedError

    def select(self, selector: str) -> list[Node]:
        from markup.element import Element

        nodes = []
        for node in self:
            if isinstance(node, Element):
                element: Element = node
                if element.matches(selector):
                    nodes.append(element)
        return nodes

    def tokens(self) -> list[str]:
        raise NotImplementedError
