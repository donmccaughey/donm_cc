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
    return text


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
            parts = line.split(' ', 2)
            yield Token(TokenType.DIRECTIVE, parts[0][1:])
            if 2 == len(parts):
                if parts[1] in modifiers:
                    yield Token(TokenType.MODIFIER, parts[1])
                else:
                    yield Token(TokenType.DATA, unescape(parts[1]))
            if 3 == len(parts):
                if parts[1] in modifiers:
                    yield Token(TokenType.MODIFIER, parts[1])
                    yield Token(TokenType.DATA, unescape(parts[2].strip()))
                else:
                    data = parts[1] + ' ' + parts[2]
                    yield Token(TokenType.DATA, unescape(data.strip()))
        else:
            paragraph.append(line.strip())
    if paragraph:
        yield Token(TokenType.PARAGRAPH, '\n'.join(paragraph))