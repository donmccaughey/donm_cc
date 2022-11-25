from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterator, Optional


class TokenType(Enum):
    DIRECTIVE = auto()
    MODIFIER = auto()
    DATA = auto()
    PARAGRAPH = auto()


@dataclass
class Location:
    line: int


@dataclass
class Token:
    type: TokenType
    text: str
    start: Location

    @staticmethod
    def data(data: str, start: Location) -> 'Token':
        return Token(TokenType.DATA, data.strip(), start)

    @staticmethod
    def directive(directive: str, start: Location) -> 'Token':
        return Token(TokenType.DIRECTIVE, directive[1:], start)

    @staticmethod
    def modifier(modifier: str, start: Location) -> 'Token':
        return Token(TokenType.MODIFIER, modifier, start)

    @staticmethod
    def paragraph(lines: list[str], start: Location) -> 'Token':
        lines = [ unescape(line.rstrip()) for line in lines ]
        return Token(TokenType.PARAGRAPH, '\n'.join(lines), start)


MODIFIERS = {
    'author', 'blog', 'book', 'docs', 'email', 'essay', 'links', 'paper',
    'podcast', 'repo', 'site'
}


def unescape(text: str) -> str:
    return text.replace(r'\.', '.')


def lexer(source: str) -> Iterator[Token]:
    paragraph = []
    paragraph_start: Optional[Location] = None
    for (i, line) in enumerate(source.splitlines()):
        line_num = i + 1
        start = Location(line_num)
        if 0 == len(line) or line.isspace():
            if paragraph:
                yield Token.paragraph(paragraph, paragraph_start)
                paragraph = []
                paragraph_start = None
        elif '.' == line[0]:
            if paragraph:
                yield Token.paragraph(paragraph, paragraph_start)
                paragraph = []
            paragraph_start = None
            directive, *rest_of_line = line.split(None, 1)
            yield Token.directive(directive, start)
            if rest_of_line:
                modifier, *data = rest_of_line[0].split(None, 1)
                if modifier in MODIFIERS:
                    yield Token.modifier(modifier, start)
                    if data:
                        yield Token.data(data[0], start)
                else:
                    yield Token.data(rest_of_line[0], start)
        else:
            paragraph.append(line)
            if not paragraph_start:
                paragraph_start = start
    if paragraph:
        yield Token.paragraph(paragraph, paragraph_start)