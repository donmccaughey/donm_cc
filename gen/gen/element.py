from typing import Optional

from .node import Node, NodeType


def q(attribute_value) -> str:
    return f"'{attribute_value}'" if ' ' in attribute_value else attribute_value


class Element(Node):
    def __init__(
            self,
            name: str,
            attributes: Optional[dict[str, str]] = None,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name=name,
            parent=parent,
            type=NodeType.ELEMENT,
            **kwargs,
        )
        self.attributes = attributes if attributes else {}

    def __str__(self):
        return self.start_tag()

    def attribute_str(self) -> str:
        if self.attributes:
            s = {f"{k}={q(v)}" for (k, v) in self.attributes.items()}
            return ' ' + ' '.join(s)
        else:
            return ''

    def start_tag(self) -> str:
        return '<' + self.name + self.attribute_str() + '>'

    def end_tag(self) -> str:
        return f'</{self.name}>'

    def write(self, f):
        f.write(self.start_tag())
        f.write('\n')
        for child in self.children:
            child.write(f)
        if len(self.children) > 0:
            f.write(self.end_tag())
            f.write('\n')
