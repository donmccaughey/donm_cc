from typing import Optional, Union

from file_formats.links_page import LinksPage, LinksSection, Link
from .lexer import Token, TokenType, lexer


def parse(source: str) -> LinksPage:
    result = Parser(source).parse()
    if isinstance(result, LinksPage):
        return result
    else:
        raise result


class ParserError(RuntimeError):
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.token = token


class MissingDirectiveError(ParserError):
    def __init__(self, token: Token, directive: str):
        self.directive = directive
        super().__init__(token, f'Expected {directive} directive')


class MissingModifierError(ParserError):
    def __init__(self, token: Token, modifier: str):
        self.modifier = modifier
        super().__init__(token, f'Expected {modifier} modifier')


class MissingDataError(ParserError):
    def __init__(self, token: Token, data_description: str):
        self.data_description = data_description
        super().__init__(token, f'Expected {data_description}')


class UnexpectedTokenError(ParserError):
    def __init__(self, token: Token):
        super().__init__(token, 'Unexpected token')


class ProductionResult:
    matched: bool
    error: Optional[ParserError]

    def __init__(self, result: Union[bool, ParserError]):
        if isinstance(result, ParserError):
            self.matched = False
            self.error = result
        else:
            self.matched = bool(result)
            self.error = None

    def __bool__(self):
        return False if self.error else self.matched


class Parser:
    """
    Parse a links file.

    Grammar:

        page = overview
             | overview sections

        overview = page_directive
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

    def __init__(self, source: str):
        self.lexer = lexer(source)
        self.token: Optional[Token] = None
        self.links_page: Optional[LinksPage] = None
        self.notes: Optional[list[str]] = None

    def parse(self) -> Union[LinksPage, ParserError]:
        self.next_token()
        result = self.page()
        if result.error:
            return result.error
        elif self.token:
            return UnexpectedTokenError(self.token)
        else:
            return self.links_page

    def page(self) -> ProductionResult:
        result = self.overview()
        if not result:
            return result
        result = self.sections()
        if result.error:
            return result
        return ProductionResult(True)

    def overview(self) -> ProductionResult:
        result = self.page_directive()
        if not result:
            return result
        result = self.paragraphs()
        if result.error:
            return result
        return ProductionResult(True)

    def page_directive(self) -> ProductionResult:
        if not self.is_directive('page'):
            return ProductionResult(MissingDirectiveError(self.token, 'page'))
        self.next_token()
        if not self.is_modifier('links'):
            return ProductionResult(MissingModifierError(self.token, 'links'))
        self.next_token()
        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'page title'))
        self.links_page = LinksPage(title=(self.token.text.strip()), notes=[], sections=[])
        self.notes = self.links_page.notes
        self.next_token()
        return ProductionResult(True)

    def paragraphs(self) -> ProductionResult:
        if not self.is_paragraph():
            return ProductionResult(False)
        self.notes.append(self.token.text)
        self.next_token()
        result = self.paragraphs()
        if result.error:
            return result
        return ProductionResult(True)

    def sections(self) -> ProductionResult:
        result = self.section()
        if not result:
            return result
        result = self.sections()
        if result.error:
            return result
        return ProductionResult(True)

    def section(self) -> ProductionResult:
        result = self.section_directive()
        if not result:
            return result
        result = self.paragraphs()
        if result.error:
            return result
        result = self.links()
        if result.error:
            return result
        return ProductionResult(True)

    def section_directive(self) -> ProductionResult:
        if not self.is_directive('section'):
            return ProductionResult(False)
        self.next_token()
        if not self.is_modifier('links'):
            return ProductionResult(MissingModifierError(self.token, 'links'))
        self.next_token()
        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'section title'))
        section = LinksSection(title=self.token.text, notes=[], links=[])
        self.links_page.sections.append(section)
        self.notes = section.notes
        self.next_token()
        return ProductionResult(True)

    def links(self) -> ProductionResult:
        result = self.link()
        if not result:
            return result
        result = self.links()
        if result.error:
            return result
        return ProductionResult(True)

    def link(self) -> ProductionResult:
        result = self.link_directive()
        if not result:
            return result
        result = self.url_directive()
        if not result:
            return result
        result = self.date_directive()
        if result.error:
            return result
        result = self.checked_directive()
        if result.error:
            return result
        return ProductionResult(True)

    def link_directive(self) -> ProductionResult:
        if not self.is_directive('link'):
            return ProductionResult(False)
        self.next_token()
        if not self.is_modifier('book'):
            return ProductionResult(MissingModifierError(self.token, 'book'))
        self.next_token()
        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'link title'))
        link = Link(
            type='book',
            title=self.token.text,
            link=None,
            date=None,
            checked=False,
        )
        self.links_page.sections[-1].links.append(link)
        self.next_token()
        return ProductionResult(True)

    def url_directive(self) -> ProductionResult:
        if not self.is_directive('url'):
            return ProductionResult(MissingDirectiveError(self.token, 'url'))
        self.next_token()
        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'URL address'))
        self.links_page.sections[-1].links[-1].link = self.token.text
        self.next_token()
        return ProductionResult(True)

    def date_directive(self) -> ProductionResult:
        if not self.is_directive('date'):
            return ProductionResult(False)
        self.next_token()
        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'date value'))
        self.links_page.sections[-1].links[-1].date = self.token.text
        self.next_token()
        return ProductionResult(True)

    def checked_directive(self) -> ProductionResult:
        if not self.is_directive('checked'):
            return ProductionResult(False)
        self.links_page.sections[-1].links[-1].checked = True
        self.next_token()
        return ProductionResult(True)

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
