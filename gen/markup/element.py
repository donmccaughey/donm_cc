from typing import Optional

from .attributes import format_attribute
from .node import Node


class Element(Node):
    def __init__(
            self,
            name: str,
            id: Optional[str] = None,
            class_names: Optional[list[str]] = None,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(name=name, parent=parent, **kwargs)
        self.attributes: dict[str, Optional[str]] = {}
        self.indent_children = True
        if id:
            self.attributes['id'] = id
        if class_names:
            self.attributes['class'] = ' '.join(class_names)

    def __repr__(self) -> str:
        return f'Element {self.start_tag()}'

    def attribute_str(self) -> str:
        if self.attributes:
            parts = [
                format_attribute(name, self.attributes[name])
                for name in self.attributes
            ]
            s = ' ' + ' '.join(parts)
            if s.endswith('/'):
                s += ' '
            return s
        else:
            return ''

    def end_tag(self) -> str:
        return f'</{self.name}>'

    def omit_end_tag(self) -> bool:
        return False

    def omit_start_tag(self) -> bool:
        return False

    def start_tag(self) -> str:
        return '<' + self.name + self.attribute_str() + '>'

    def markup(self, width: int) -> str:
        markup = self.start_tag()
        for child in self.children:
            markup += child.markup(width)
        markup += self.end_tag()
        markup += '\n'
        return markup

    def matches(self, single_selector: str) -> bool:
        assert ' ' not in single_selector

        if ':' in single_selector:
            single_selector = single_selector.split(':')[0]

        if single_selector.startswith('#'):
            assert len(single_selector) > 1
            return self.attributes.get('id') == single_selector[1:]
        elif single_selector.startswith('.'):
            assert len(single_selector) > 1
            class_names = self.attributes.get('class', '').split()
            return single_selector[1:] in class_names
        else:
            assert len(single_selector)
            return self.name == single_selector
