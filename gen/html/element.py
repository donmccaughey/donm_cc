from enum import unique, Enum, auto
from textwrap import indent
from typing import Optional
from .node import Node
from .tag import Tag, TagType


def q(attribute_value) -> str:
    return f"'{attribute_value}'" if ' ' in attribute_value else attribute_value


def format_attribute(name: str, value: Optional[str]) -> str:
    if value:
        return f'{name}={q(value)}'
    else:
        return name


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
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name=name,
            parent=parent,
            **kwargs,
        )
        self.attributes: dict[str, str] = {}
        self.element_type = element_type
        self.has_end_tag = True
        self.indent_children = True
        self.is_heading = False
        self.is_phrasing_content = False
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
        # TODO: html encode attribute values
        if self.attributes:
            parts = [
                format_attribute(name, self.attributes[name])
                for name in self.attributes
            ]
            return ' ' + ' '.join(parts)
        else:
            return ''

    def end_tag(self) -> str:
        return f'</{self.name}>'

    def start_tag(self) -> str:
        return '<' + self.name + self.attribute_str() + '>'

    def tags(self) -> list[Tag]:
        tags = [
            Tag(
                name=self.name,
                text=self.start_tag(),
                type=TagType.START,
                format=self.format,
                has_end_tag=self.has_end_tag,
                indent_children=self.indent_children,
                is_heading=self.is_heading,
                is_phrasing_content=self.is_phrasing_content,
            )
        ]
        for child in self.children:
            tags += child.tags()
        tags+= [
            Tag(
                name=self.name,
                text=self.end_tag() if self.has_end_tag else '',
                type=TagType.END,
                format=self.format,
                has_end_tag=self.has_end_tag,
                indent_children=self.indent_children,
                is_heading=self.is_heading,
                is_phrasing_content=self.is_phrasing_content,
            )
        ]
        return tags
