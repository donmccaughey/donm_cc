from typing import Optional, List

from .node import Node
from .wrap import wrap_tokens


class Text(Node):
    def __init__(self, text: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='text',
            parent=parent,
            **kwargs,
        )
        assert text
        self.text = text

    def markup(self, width: int) -> str:
        return ''.join(wrap_tokens(self.tokens(), width))

    def tokens(self) -> List[str]:
        # TODO: HTML encode text
        tokens = []
        token_is_space = self.text[0].isspace()
        token = ''
        for ch in self.text:
            ch_is_space = ch.isspace()
            if token and ch_is_space != token_is_space:
                tokens.append(token)
                token = ''
                token_is_space = ch_is_space
            if ch_is_space:
                token = ' '
            else:
                token += ch
        tokens.append(token)
        return tokens
