from typing import Optional, Any

from file_formats.page_file import PageFile, LinksSection, Link, BookLink
from .lexer import Token, TokenType, lexer


LINK_MODIFIERS = ('blog', 'docs', 'email', 'podcast', 'repo', 'site')


def parse(source: str) -> PageFile:
    result = Parser(source).parse()
    if isinstance(result, PageFile):
        return result
    else:
        raise result


class ParserError(RuntimeError):
    def __init__(self, token: Token, message: str):
        if token:
            message = f'{token.start.line}: {message}'
        super().__init__(message)
        self.token = token


class MissingDirectiveError(ParserError):
    def __init__(self, token: Token, directive: str):
        self.directive = directive
        super().__init__(token, f'Expected `.{directive}` directive')


class MissingLinkModifierError(ParserError):
    def __init__(self, token: Token):
        super().__init__(token, f'Expected `.link` modifier: {LINK_MODIFIERS}')


class MissingModifierError(ParserError):
    def __init__(self, token: Token, modifier: str):
        self.modifier = modifier
        super().__init__(token, f'Expected `{modifier}` modifier')


class MissingDataError(ParserError):
    def __init__(self, token: Token, data_description: str):
        self.data_description = data_description
        super().__init__(token, f'Expected {data_description}')


class UnexpectedTokenError(ParserError):
    def __init__(self, token: Token):
        super().__init__(token, 'Unexpected token')


class ProductionResult:
    def __init__(self, result: bool | ParserError, value: Optional[Any] = None):
        if isinstance(result, ParserError):
            self.matched = False
            self.error = result
        else:
            self.matched = bool(result)
            self.error = None
        self.value = value

    def __bool__(self):
        return False if self.error else self.matched


class Parser:
    """
    Parse a page file.

    Grammar:

        page = overview
             | overview sections

        overview = page_attributes
                 | page_attributes paragraphs

        page_attributes = page_directive
                        | page_directive subtitle_directive

        page_directive = '.page' 'links' DATA

        subtitle_directive = '.subtitle' DATA

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

        link = '.link' book_link
             | '.link' general_link

        book_link = book_link_directive book_locator
                  | book_link_directive book_locator link_attributes

        book_link_directive = 'book' DATA

        book_locator = asin_directive
                     | url_directive
                     | asin_directive url_directive
                     | url_directive asin_directive

        url_directive = '.url' DATA

        asin_directive = '.asin' DATA

        link_attributes = link_attribute
                        | link_attribute link_attributes

        link_attribute = author_directive
                       | date_directive
                       | checked_directive

        author_directive = '.author' DATA

        date_directive = '.date' DATA

        checked_directive = '.checked'

        general_link = general_link_directive url_directive
                     | general_link_directive url_directive link_attributes

        general_link_directive = general_link_modifier DATA

        general_link_modifier = 'blog' | 'docs' | 'email' | 'podcast' | 'repo' | 'site'
    """

    def __init__(self, source: str):
        self.lexer = lexer(source)
        self.token: Optional[Token] = None
        self.page_file: Optional[PageFile] = None
        self.notes: Optional[list[str]] = None

    def parse(self) -> PageFile | ParserError:
        self.next_token()
        result = self.page()
        if result.error:
            return result.error
        elif self.token:
            return UnexpectedTokenError(self.token)
        else:
            return self.page_file

    def page(self) -> ProductionResult:
        result = self.overview()
        if not result:
            return result
        result = self.sections()
        if result.error:
            return result
        return ProductionResult(True)

    def overview(self) -> ProductionResult:
        result = self.page_attributes()
        if not result:
            return result
        result = self.paragraphs()
        if result.error:
            return result
        return ProductionResult(True)

    def page_attributes(self) -> ProductionResult:
        result = self.page_directive()
        if not result:
            return result
        result = self.subtitle_directive()
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
        self.page_file = PageFile(
            title=(self.token.text.strip()),
            subtitle=None,
            notes=[],
            sections=[]
        )
        self.notes = self.page_file.notes
        self.next_token()
        return ProductionResult(True)

    def subtitle_directive(self) -> ProductionResult:
        if not self.is_directive('subtitle'):
            return ProductionResult(False)
        self.next_token()
        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'page subtitle'))
        self.page_file.subtitle = self.token.text.strip()
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
        self.page_file.sections.append(section)
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
        if not self.is_directive('link'):
            return ProductionResult(False)
        self.next_token()
        result = self.book_link()
        if result.matched or result.error:
            return result
        return self.general_link()

    def book_link(self) -> ProductionResult:
        result = self.book_link_directive()
        if not result:
            return result
        link = result.value
        self.page_file.sections[-1].links.append(link)

        result = self.book_locator(link)
        if not result:
            return result

        result = self.link_attributes(link)
        if result.error:
            return result

        return ProductionResult(True)

    def book_link_directive(self) -> ProductionResult:
        if not self.is_modifier('book'):
            return ProductionResult(False)
        self.next_token()
        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'link title'))
        link = BookLink(
            modifier='book',
            title=self.token.text,
            url=None,
            asin=None,
            authors=[],
            date=None,
            checked=False,
        )
        result = ProductionResult(True, value=link)
        self.next_token()
        return result

    def book_locator(self, link: BookLink) -> ProductionResult:
        result = self.asin_directive()
        if result.matched:
            link.asin = result.value
            result = self.url_directive()
            if result.matched:
                link.url = result.value
                return result
            return ProductionResult(True)

        result = self.url_directive()
        if result.error:
            return result
        if result.matched:
            link.url = result.value
            result = self.asin_directive()
            if result.matched:
                link.asin = result.value
                return result
            return ProductionResult(True)

        return ProductionResult(False)

    def url_directive(self) -> ProductionResult:
        if not self.is_directive('url'):
            return ProductionResult(MissingDirectiveError(self.token, 'url'))
        self.next_token()

        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'URL address'))
        result = ProductionResult(True, value=self.token.text)
        self.next_token()
        return result

    def asin_directive(self) -> ProductionResult:
        if not self.is_directive('asin'):
            return ProductionResult(MissingDirectiveError(self.token, 'asin'))
        self.next_token()

        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'ASIN'))
        self.page_file.sections[-1].links[-1].asin = self.token.text
        result = ProductionResult(True, value=self.token.text)
        self.next_token()
        return result

    def link_attributes(self, link: Link | BookLink) -> ProductionResult:
        result = self.link_attribute(link)
        if not result:
            return result
        result = self.link_attributes(link)
        if result.error:
            return result
        return ProductionResult(True)

    def link_attribute(self, link: BookLink | Link) -> ProductionResult:
        result = self.author_directive()
        if result.error:
            return result
        if result.matched:
            link.authors.append(result.value)
            return result

        result = self.date_directive()
        if result.error:
            return result
        if result.matched:
            link.date = result.value
            return result

        result = self.checked_directive()
        if result.error:
            return result
        if result.matched:
            link.checked = True
            return result

        return ProductionResult(False)

    def general_link(self) -> ProductionResult:
        result = self.general_link_directive()
        if not result:
            return result
        link = result.value
        self.page_file.sections[-1].links.append(link)

        result = self.url_directive()
        if not result:
            return result
        link.url = result.value

        result = self.link_attributes(link)
        if result.error:
            return result

        return ProductionResult(True)

    def general_link_directive(self) -> ProductionResult:
        if not self.is_general_link_modifier():
            return ProductionResult(MissingLinkModifierError(self.token))
        modifier = self.token.text
        self.next_token()
        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'link title'))
        link = Link(
            modifier=modifier,
            title=self.token.text,
            url=None,
            authors=[],
            date=None,
            checked=False,
        )
        result = ProductionResult(True, value=link)
        self.next_token()
        return result

    def author_directive(self) -> ProductionResult:
        if not self.is_directive('author'):
            return ProductionResult(False)
        self.next_token()
        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'author value'))
        result = ProductionResult(True, value=self.token.text)
        self.next_token()
        return result

    def date_directive(self) -> ProductionResult:
        if not self.is_directive('date'):
            return ProductionResult(False)
        self.next_token()
        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'date value'))
        result = ProductionResult(True, value=self.token.text)
        self.next_token()
        return result

    def checked_directive(self) -> ProductionResult:
        if not self.is_directive('checked'):
            return ProductionResult(False)
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

    def is_general_link_modifier(self) -> bool:
        return (
                self.token
                and TokenType.MODIFIER == self.token.type
                and self.token.text in LINK_MODIFIERS
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
