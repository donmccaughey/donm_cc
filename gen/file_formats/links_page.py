from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Iterator, Union

from markup import Section, H1, P, Ul
from resources import Page
from website.links import link as build_link


@dataclass
class Link:
    type: str
    title: str
    link: Optional[str]
    date: Optional[str]
    checked: bool


@dataclass
class LinksSection:
    title: str
    notes: list[str]
    links: list[Link]


@dataclass
class LinksPage:
    title: str
    notes: list[str]
    sections: list[LinksSection]

    def build(self):
        with Page(self.title):
            with Section(class_names=['overview']):
                H1(self.title)
                for note in self.notes:
                    P(note)
            for section in self.sections:
                with Section(class_names=['links']):
                    H1(section.title)
                    for note in section.notes:
                        P(note)
                    with Ul():
                        for link in section.links:
                            build_link(
                                type=link.type,
                                title=link.title,
                                href=link.link,
                                authors=None,
                                date=link.date,
                                checked=link.checked,
                            )


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


def tokenize(source: str) -> Iterator[Token]:
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


class ParserError(RuntimeError):
    def __init__(self, token: Token, message: str):
        super().__init__(message)


class Parser:
    """
    Parse a links file.

    Grammar:

        page = declaration
             | declaration sections

        declaration = page_directive
                    | page_directive paragraphs

        page_directive = '.page' 'links' DATA

        paragraphs = PARAGRAPH
                   | PARAGRAPH paragraphs

        sections = section
                 | section sections

        section = section_directive
                | section_directive paragraphs
                | section_directive paragraphs links
                | section_directive links

        section_directive = '.section' 'links' DATA

        links = link
              | link links

        link = link_directive url_directive
             | link_directive url_directive date_directive
             | link_directive url_directive date_directive checked_directive
             | link_directive url_directive checked_directive

        link_directive = '.link' 'book' DATA

        url_directive = '.url' DATA

        date_directive = '.date' DATA

        checked_directive = '.checked'
    """

    def __init__(self, lexer: Iterator[Token]):
        self.lexer = lexer
        self.token: Optional[Token] = None
        self.error: Optional[ParserError] = None
        self.links_page: Optional[LinksPage] = None
        self.notes: Optional[list[str]] = None

    def parse(self) -> Union[LinksPage, ParserError]:
        self.next_token()
        # TODO: detect incomplete parse
        parsed = self.page()
        return self.links_page if parsed else self.error

    def next_token(self):
        try:
            self.token = next(self.lexer)
        except StopIteration:
            self.token = None

    def is_data(self) -> bool:
        return (
            self.token
            and TokenType.DATA == self.token.type
        )

    def is_directive(self, directive) -> bool:
        return (
            self.token
            and TokenType.DIRECTIVE == self.token.type
            and directive == self.token.text
        )

    def is_modifier(self, modifier) -> bool:
        return (
            self.token
            and TokenType.MODIFIER == self.token.type
            and modifier == self.token.text
        )

    def is_paragraph(self) -> bool:
        return (
            self.token
            and TokenType.PARAGRAPH == self.token.type
        )

    def page(self) -> bool:
        if not self.declaration():
            return False
        self.sections()
        return True

    def declaration(self) -> bool:
        if not self.page_directive():
            return False
        self.paragraphs()
        return True

    def page_directive(self) -> bool:
        if not self.is_directive('page'):
            self.error = ParserError(self.token, 'Expected .page directive')
            return False
        self.next_token()
        if not self.is_modifier('links'):
            self.error = ParserError(self.token, 'Expected links modifier')
            return False
        self.next_token()
        if not self.is_data():
            self.error = ParserError(self.token, 'Expected page title')
            return False
        self.links_page = LinksPage(title=(self.token.text.strip()), notes=[], sections=[])
        self.notes = self.links_page.notes
        self.next_token()
        return True

    def paragraphs(self) -> bool:
        if not self.is_paragraph():
            self.error = ParserError(self.token, 'Expected a paragraph')
            return False
        self.notes.append(self.token.text)
        self.next_token()
        self.paragraphs()
        return True

    def sections(self) -> bool:
        if not self.section():
            return False
        self.sections()
        return True

    def section(self) -> bool:
        if not self.section_directive():
            return False
        if self.paragraphs():
            self.links()
        else:
            self.links()
        return True

    def section_directive(self) -> bool:
        if not self.is_directive('section'):
            self.error = ParserError(self.token, 'Expected .section directive')
            return False
        self.next_token()
        if not self.is_modifier('links'):
            self.error = ParserError(self.token, 'Expected links modifier')
            return False
        self.next_token()
        if not self.is_data():
            self.error = ParserError(self.token, 'Expected section title')
            return False
        section = LinksSection(title=self.token.text, notes=[], links=[])
        self.links_page.sections.append(section)
        self.notes = section.notes
        self.next_token()
        return True

    def links(self) -> bool:
        if not self.link():
            return False
        self.links()
        return True

    def link(self) -> bool:
        if not self.link_directive():
            return False
        if not self.url_directive():
            return False
        if self.date_directive():
            self.checked_directive()
        else:
            self.checked_directive()
        return True

    def link_directive(self) -> bool:
        if not self.is_directive('link'):
            self.error = ParserError(self.token, 'Expected .links directive')
            return False
        self.next_token()
        if not self.is_modifier('book'):
            self.error = ParserError(self.token, 'Expected book modifier')
            return False
        self.next_token()
        if not self.is_data():
            self.error = ParserError(self.token, 'Expected link title')
            return False
        link = Link(
            type='book',
            title=self.token.text,
            link=None,
            date=None,
            checked=False,
        )
        self.links_page.sections[-1].links.append(link)
        self.next_token()
        return True

    def url_directive(self) -> bool:
        if not self.is_directive('url'):
            self.error = ParserError(self.token, 'Expected .url directive')
            return False
        self.next_token()
        if not self.is_data():
            self.error = ParserError(self.token, 'Expected URL')
            return False
        self.links_page.sections[-1].links[-1].link = self.token.text
        self.next_token()
        return True

    def date_directive(self) -> bool:
        if not self.is_directive('date'):
            self.error = ParserError(self.token, 'Expected .date directive')
            return False
        self.next_token()
        if not self.is_data():
            self.error = ParserError(self.token, 'Expected date')
            return False
        self.links_page.sections[-1].links[-1].date = self.token.text
        self.next_token()
        return True

    def checked_directive(self) -> bool:
        if not self.is_directive('checked'):
            self.error = ParserError(self.token, 'Expected .checked directive')
            return False
        self.links_page.sections[-1].links[-1].checked = True
        self.next_token()
        return True
