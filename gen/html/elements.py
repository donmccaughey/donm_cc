from typing import Optional

from html.element import Element
from html.node import Node


class Li(Element):
    def __init__(
            self,
            id: Optional[str] = None,
            class_names: Optional[list[str]] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='li',
            id=id,
            class_names=class_names,
            parent=parent,
            **kwargs,
        )


class Script(Element):
    def __init__(
            self,
            src: str,
            charset: Optional[str] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(name='script', parent=parent, **kwargs)
        if charset:
            self.attributes['charset'] = charset
        self.attributes['src'] = src
        self.attributes['type'] = 'text/javascript'
