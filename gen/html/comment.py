from typing import Optional
from .node import Node
from .tag import Tag
from .tag_type import TagType


class Comment(Node):
    def __init__(self, text: str, parent: Optional[Node]=None, **kwargs):
        super().__init__(
            name='comment',
            parent=parent,
            **kwargs,
        )
        self.text = text

    def markup(self, width: int) -> str:
        # TODO: handle invalid comment text
        # https://www.w3.org/TR/html52/syntax.html#comments
        # Optionally, text, with the additional restriction that the text must
        # not start with the string ">", nor start with the string "->", nor
        # contain the strings "<!--", "-->", or "--!>", nor end with the
        # string "<!-".
        return f'<!-- {self.text} -->\n'

    def tags(self) -> list[Tag]:
        return [
            Tag(
                name=self.name,
                text=f'<!-- {self.text} -->',
                type=TagType.COMMENT,
                format=self.format,
                omit=False,
                indent_children=False,
            )
        ]
