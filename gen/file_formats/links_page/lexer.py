from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterator


class TokenType(Enum):
    DIRECTIVE = auto()
    MODIFIER = auto()
    DATA = auto()
    PARAGRAPH = auto()


@dataclass
class Token:
    type: TokenType
    text: str


modifiers = ['links', 'book']


def unescape(text: str) -> str:
    return text.replace(r'\.', '.')


def lexer(source: str) -> Iterator[Token]:
    paragraph = []
    for line in source.splitlines():
        if 0 == len(line) or line.isspace():
            if paragraph:
                yield Token(TokenType.PARAGRAPH, '\n'.join(paragraph))
                paragraph = []
        elif '.' == line[0]:
            if paragraph:
                yield Token(TokenType.PARAGRAPH, '\n'.join(paragraph))
                paragraph = []
            directive, *rest_of_line = line.split(None, 1)
            yield Token(TokenType.DIRECTIVE, directive[1:])
            if rest_of_line:
                modifier, *data = rest_of_line[0].split(None, 1)
                if modifier in modifiers:
                    yield Token(TokenType.MODIFIER, modifier)
                    if data:
                        yield Token(TokenType.DATA, data[0].strip())
                else:
                    yield Token(TokenType.DATA, rest_of_line[0].strip())
        else:
            paragraph.append(unescape(line.rstrip()))
    if paragraph:
        yield Token(TokenType.PARAGRAPH, '\n'.join(paragraph))