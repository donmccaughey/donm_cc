from typing import Optional, List

import re
from .node import Node
from .wrap import wrap_tokens


# See https://html.spec.whatwg.org/multipage/syntax.html#character-references
CHAR_REF = re.compile(r'&#?\w+;')


def html_encode(text: str) -> str:
    if re.search(CHAR_REF, text):
        text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    return text


class Text(Node):
    def __init__(
            self,
            text: str,
            preformatted: bool = False,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name='text',
            parent=parent,
            **kwargs,
        )
        assert text
        self.preformatted = preformatted
        self.text = text

    def markup(self, width: int) -> str:
        if self.preformatted:
            return self.text
        else:
            return ''.join(wrap_tokens(self.tokens(), width))

    def tokens(self) -> List[str]:
        if self.preformatted:
            return [html_encode(self.text.strip())]

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
        return [html_encode(token) for token in tokens]
