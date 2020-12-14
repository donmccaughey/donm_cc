import textwrap
from typing import Optional

from .node import Node


class Text(Node):
    def __init__(
            self,
            text: str,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name='text',
            parent=parent,
            **kwargs,
        )
        self.text = text

    def __str__(self) -> str:
        # TODO: HTML encode text
        return textwrap.fill(self.text.strip())
