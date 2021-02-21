from typing import Iterator, Optional, Union

from file_formats.links_page import LinksPage, LinksSection, Link
from .lexer import Token, TokenType


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