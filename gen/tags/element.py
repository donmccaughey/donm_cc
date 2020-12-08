from enum import unique, Enum, auto
from textwrap import indent
from typing import Optional

from .node import Node, NodeType


def q(attribute_value) -> str:
    return f"'{attribute_value}'" if ' ' in attribute_value else attribute_value


@unique
class ElementType(Enum):
    CONTAINER = auto()
    COMPACT = auto()
    EMPTY = auto()


class Element(Node):
    def __init__(
            self,
            name: str,
            id: Optional[str] = None,
            class_names: Optional[list[str]] = None,
            element_type: ElementType = ElementType.CONTAINER,
            indent_children: bool = True,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name=name,
            node_type=NodeType.ELEMENT,
            parent=parent,
            **kwargs,
        )
        self.attributes: dict[str, str] = {}
        self.element_type = element_type
        self.indent_children = indent_children
        if id:
            self.attributes['id'] = id
        if class_names:
            self.attributes['class'] = ' '.join(class_names)

    def __str__(self) -> str:
        if self.element_type == ElementType.COMPACT:
            s = self.start_tag()
            for child in self.children:
                s += str(child)
            s += self.end_tag()
            return s
        elif self.element_type == ElementType.EMPTY:
            return self.start_tag()
        else:
            s = self.start_tag()
            s += '\n'
            for child in self.children:
                child = str(child) + '\n'
                s += indent(child, '    ') if self.indent_children else child
            s += self.end_tag()
            return s

    def attribute_str(self) -> str:
        if self.attributes:
            parts = [
                f'{name}={q(self.attributes[name])}' for name in self.attributes
            ]
            return ' ' + ' '.join(parts)
        else:
            return ''

    def end_tag(self) -> str:
        return f'</{self.name}>'

    def start_tag(self) -> str:
        return '<' + self.name + self.attribute_str() + '>'
