from textwrap import indent
from typing import Optional

from .element_type import ElementType
from .node import Node
from .tag import Tag
from .tag_type import TagType


def q(attribute_value) -> str:
    return f"'{attribute_value}'" if ' ' in attribute_value else attribute_value


def format_attribute(name: str, value: Optional[str]) -> str:
    if value:
        return f'{name}={q(value)}'
    else:
        return name


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
        self.indent_children = True
        if id:
            self.attributes['id'] = id
        if class_names:
            self.attributes['class'] = ' '.join(class_names)

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
                omit=False,
                indent_children=self.indent_children,
            )
        ]
        for child in self.children:
            tags += child.tags()
        tags += [
            Tag(
                name=self.name,
                text=self.end_tag(),
                type=TagType.END,
                format=self.format,
                omit=self.element_type == ElementType.EMPTY,
                indent_children=self.indent_children,
            )
        ]
        return tags
