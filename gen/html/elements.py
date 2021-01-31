from typing import Optional

from html.element import Element
from html.node import Node




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
