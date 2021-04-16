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

    @staticmethod
    def data(data: str) -> 'Token':
        return Token(TokenType.DATA, data.strip())

    @staticmethod
    def directive(directive: str) -> 'Token':
        return Token(TokenType.DIRECTIVE, directive[1:])

    @staticmethod
    def modifier(modifier: str) -> 'Token':
        return Token(TokenType.MODIFIER, modifier)

    @staticmethod
    def paragraph(lines: list[str]) -> 'Token':
        lines = [ unescape(line.rstrip()) for line in lines ]
        return Token(TokenType.PARAGRAPH, '\n'.join(lines))


MODIFIERS = (
    'blog', 'book', 'docs', 'email', 'links', 'podcast', 'repo', 'site'
)


def unescape(text: str) -> str:
    return text.replace(r'\.', '.')


def lexer(source: str) -> Iterator[Token]:
    paragraph = []
    for line in source.splitlines():
        if 0 == len(line) or line.isspace():
            if paragraph:
                yield Token.paragraph(paragraph)
                paragraph = []
        elif '.' == line[0]:
            if paragraph:
                yield Token.paragraph(paragraph)
                paragraph = []
            directive, *rest_of_line = line.split(None, 1)
            yield Token.directive(directive)
            if rest_of_line:
                modifier, *data = rest_of_line[0].split(None, 1)
                if modifier in MODIFIERS:
                    yield Token.modifier(modifier)
                    if data:
                        yield Token.data(data[0])
                else:
                    yield Token.data(rest_of_line[0])
        else:
            paragraph.append(line)
    if paragraph:
        yield Token.paragraph(paragraph)