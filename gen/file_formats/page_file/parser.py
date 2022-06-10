from typing import Optional, TypeVar, Generic, Any, List, Tuple

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


V = TypeVar('V')


class ProductionResult(Generic[V]):
    def __init__(self, result: bool | ParserError, value: Optional[V] = None):
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
        if result.matched:
            self.page_file.sections = result.value
        return ProductionResult(True)

    def overview(self) -> ProductionResult:
        result = self.page_attributes()
        if not result:
            return result
        title, subtitle = result.value

        notes = []
        result = self.paragraphs()
        if result.error:
            return result
        if result.matched:
            notes = result.value

        self.page_file = PageFile(
            title=title,
            subtitle=subtitle,
            notes=notes,
            sections=[]
        )
        return ProductionResult(True)

    def page_attributes(self) -> ProductionResult[Tuple[str, Optional[str]]]:
        result = self.page_directive()
        if not result:
            return result
        title = result.value

        subtitle = None
        result = self.subtitle_directive()
        if result.error:
            return result
        if result.matched:
            subtitle = result.value

        return ProductionResult(True, value=(title, subtitle))

    def page_directive(self) -> ProductionResult[str]:
        if not self.is_directive('page'):
            return ProductionResult(MissingDirectiveError(self.token, 'page'))
        self.next_token()

        if not self.is_modifier('links'):
            return ProductionResult(MissingModifierError(self.token, 'links'))
        self.next_token()

        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'page title'))
        title = self.token.text.strip()
        self.next_token()

        return ProductionResult(True, value=title)

    def subtitle_directive(self) -> ProductionResult[str]:
        if not self.is_directive('subtitle'):
            return ProductionResult(False)
        self.next_token()

        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'page subtitle'))
        subtitle = self.token.text.strip()
        self.next_token()

        return ProductionResult(True, value=subtitle)

    def paragraphs(self) -> ProductionResult[List[str]]:
        if not self.is_paragraph():
            return ProductionResult(False)
        paragraph = self.token.text
        self.next_token()

        result = self.paragraphs()
        if result.error:
            return result
        paragraphs = result.value if result.matched else []
        return ProductionResult(True, value=[paragraph] + paragraphs)

    def sections(self) -> ProductionResult[List[LinksSection]]:
        result = self.section()
        if not result:
            return result
        section = result.value

        result = self.sections()
        if result.error:
            return result
        sections = result.value if result.matched else []
        return ProductionResult(True, value=[section] + sections)

    def section(self) -> ProductionResult[LinksSection]:
        result = self.section_directive()
        if not result:
            return result
        title = result.value

        result = self.paragraphs()
        if result.error:
            return result
        notes = result.value if result.matched else []

        result = self.links()
        if result.error:
            return result
        links = result.value if result.matched else []

        section = LinksSection(title=title, notes=notes, links=links)
        return ProductionResult(True, value=section)

    def section_directive(self) -> ProductionResult[str]:
        if not self.is_directive('section'):
            return ProductionResult(False)
        self.next_token()

        if not self.is_modifier('links'):
            return ProductionResult(MissingModifierError(self.token, 'links'))
        self.next_token()

        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'section title'))
        title = self.token.text
        self.next_token()

        return ProductionResult(True, value=title)

    def links(self) -> ProductionResult[List[BookLink | Link]]:
        result = self.link()
        if not result:
            return result
        link = result.value

        result = self.links()
        if result.error:
            return result
        links = result.value if result.matched else []
        return ProductionResult(True, value=[link] + links)

    def link(self) -> ProductionResult[BookLink | Link]:
        if not self.is_directive('link'):
            return ProductionResult(False)
        self.next_token()

        for x_link in [self.book_link, self.general_link]:
            result = x_link()
            if result.matched or result.error:
                return result
        return ProductionResult(False)

    def book_link(self) -> ProductionResult[BookLink]:
        result = self.book_link_directive()
        if not result:
            return result
        title = result.value

        result = self.book_locator()
        if not result:
            return result
        asin, url = result.value

        link = BookLink(
            modifier='book',
            title=title,
            url=url,
            asin=asin,
            authors=[],
            date=None,
            checked=False,
        )
        result = self.link_attributes(link)
        if result.error:
            return result

        return ProductionResult(True, value=link)

    def book_link_directive(self) -> ProductionResult[str]:
        if not self.is_modifier('book'):
            return ProductionResult(False)
        self.next_token()

        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'link title'))
        title = self.token.text
        self.next_token()

        return ProductionResult(True, value=title)

    def book_locator(self) -> ProductionResult[Tuple[Optional[str], Optional[str]]]:
        asin, url = None, None

        result = self.asin_directive()
        if result.matched:
            asin = result.value
            result = self.url_directive()
            if result.matched:
                url = result.value
            return ProductionResult(True, value=(asin, url))

        result = self.url_directive()
        if result.error:
            return result
        if result.matched:
            url = result.value
            result = self.asin_directive()
            if result.matched:
                asin = result.value
            return ProductionResult(True, value=(asin, url))

        return ProductionResult(False)

    def url_directive(self) -> ProductionResult[str]:
        if not self.is_directive('url'):
            return ProductionResult(MissingDirectiveError(self.token, 'url'))
        self.next_token()

        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'URL address'))
        url = self.token.text
        self.next_token()

        return ProductionResult(True, value=url)

    def asin_directive(self) -> ProductionResult[str]:
        if not self.is_directive('asin'):
            return ProductionResult(MissingDirectiveError(self.token, 'asin'))
        self.next_token()

        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'ASIN'))
        asin = self.token.text
        self.next_token()

        return ProductionResult(True, value=asin)

    def link_attributes(self, link: Link | BookLink) -> ProductionResult[Any]:
        result = self.link_attribute(link)
        if not result:
            return result
        result = self.link_attributes(link)
        if result.error:
            return result
        return ProductionResult(True)

    def link_attribute(self, link: BookLink | Link) -> ProductionResult[Any]:
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

    def general_link(self) -> ProductionResult[Link]:
        result = self.general_link_directive()
        if not result:
            return result
        modifier, title = result.value
        link = Link(
            modifier=modifier,
            title=title,
            url=None,
            authors=[],
            date=None,
            checked=False,
        )

        result = self.url_directive()
        if not result:
            return result
        link.url = result.value

        result = self.link_attributes(link)
        if result.error:
            return result

        return ProductionResult(True, value=link)

    def general_link_directive(self) -> ProductionResult[Tuple[str, str]]:
        if not self.is_general_link_modifier():
            return ProductionResult(MissingLinkModifierError(self.token))
        modifier = self.token.text
        self.next_token()

        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'link title'))
        title = self.token.text
        self.next_token()

        return ProductionResult(True, value=(modifier, title))

    def author_directive(self) -> ProductionResult[str]:
        if not self.is_directive('author'):
            return ProductionResult(False)
        self.next_token()
        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'author value'))
        author = self.token.text
        self.next_token()

        return ProductionResult(True, value=author)

    def date_directive(self) -> ProductionResult[str]:
        if not self.is_directive('date'):
            return ProductionResult(False)
        self.next_token()

        if not self.is_data():
            return ProductionResult(MissingDataError(self.token, 'date value'))
        date = self.token.text
        self.next_token()

        return ProductionResult(True, value=date)

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
