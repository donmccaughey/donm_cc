from dataclasses import dataclass
from typing import Optional, TypeVar, Generic, List, Tuple

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


class NotMatched:
    pass


V = TypeVar('V')


@dataclass
class Matched(Generic[V]):
    value: V


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

    def parse(self) -> PageFile | ParserError:
        self.next_token()
        result = self.page()
        if result.error:
            return result.error
        if self.token:
            return UnexpectedTokenError(self.token)
        return result.value

    def page(self) -> ProductionResult[PageFile]:
        result = self.overview()
        if not result:
            return result
        title, subtitle, notes = result.value

        result = self.sections()
        if result.error:
            return result
        sections = result.value if result.matched else []

        page = PageFile(
            title=title,
            subtitle=subtitle,
            notes=notes,
            sections=sections
        )
        return ProductionResult(True, value=page)

    def overview(self) -> ProductionResult[Tuple[str, Optional[str], List[str]]]:
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

        return ProductionResult(True, value=(title, subtitle, notes))

    def page_attributes(self) -> ProductionResult[Tuple[str, Optional[str]]]:
        result = self.page_directive()
        if not result:
            return result
        title = result.value

        match self.subtitle_directive():
            case Matched(value):
                subtitle = value
            case NotMatched():
                subtitle = None
            case ParserError() as e:
                return ProductionResult(e)

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

    def subtitle_directive(self) -> Matched[str] | NotMatched | ParserError:
        if not self.is_directive('subtitle'):
            return NotMatched()
        self.next_token()

        if not self.is_data():
            return MissingDataError(self.token, 'page subtitle')
        subtitle = self.token.text.strip()
        self.next_token()

        return Matched(subtitle)

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

        result = self.link_attributes()
        if result.error:
            return result
        authors = []
        date = None
        checked = False
        if result.matched:
            for name, value in result.value:
                if 'author' == name:
                    authors.append(value)
                elif 'date' == name:
                    # TODO: return error on duplicate date attribute
                    date = value
                elif 'checked' == name:
                    # TODO: return error on duplicate checked attribute
                    checked = True
                else:
                    raise RuntimeError(f'Unexpected link attribute type "{name}"')

        link = BookLink(
            modifier='book',
            title=title,
            url=url,
            asin=asin,
            authors=authors,
            date=date,
            checked=checked,
        )
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
        match self.asin_directive():
            case Matched(value):
                asin = value
                match self.url_directive():
                    case Matched(value):
                        url = value
                    case ParserError():
                        url = None
                return ProductionResult(True, value=(asin, url))
            case ParserError():
                pass

        match self.url_directive():
            case Matched(value):
                url = value
                match self.asin_directive():
                    case Matched(value):
                        asin = value
                    case ParserError():
                        asin = None
                return ProductionResult(True, value=(asin, url))
            case ParserError() as e:
                return ProductionResult(e)

        return ProductionResult(False)

    def url_directive(self) -> Matched[str] | ParserError:
        if not self.is_directive('url'):
            return MissingDirectiveError(self.token, 'url')
        self.next_token()

        if not self.is_data():
            return MissingDataError(self.token, 'URL address')
        url = self.token.text
        self.next_token()

        return Matched(url)

    def asin_directive(self) -> Matched[str] | ParserError:
        if not self.is_directive('asin'):
            return MissingDirectiveError(self.token, 'asin')
        self.next_token()

        if not self.is_data():
            return MissingDataError(self.token, 'ASIN')
        asin = self.token.text
        self.next_token()

        return Matched(asin)

    def link_attributes(self) -> ProductionResult[List[Tuple[str, str]]]:
        match self.link_attribute():
            case Matched(value):
                attribute = value
            case NotMatched():
                return ProductionResult(False)
            case ParserError() as e:
                return ProductionResult(e)

        result = self.link_attributes()
        if result.error:
            return result
        attributes = result.value if result.matched else []
        return ProductionResult(True, value=[attribute] + attributes)

    def link_attribute(self) -> Matched[Tuple[str, str]] | NotMatched | ParserError:
        match self.author_directive():
            case Matched(value=author):
                return Matched(('author', author))
            case NotMatched():
                pass
            case ParserError() as e:
                return e

        match self.date_directive():
            case Matched(value=date):
                return Matched(('date', date))
            case NotMatched():
                pass
            case ParserError() as e:
                return e

        match self.checked_directive():
            case Matched():
                return Matched(('checked', ''))
            case NotMatched():
                pass

        return NotMatched()

    def general_link(self) -> ProductionResult[Link]:
        match self.general_link_directive():
            case Matched(value):
                modifier, title = value
            case ParserError() as e:
                return ProductionResult(e)

        match self.url_directive():
            case Matched(value):
                url = value
            case ParserError() as e:
                return ProductionResult(e)

        result = self.link_attributes()
        if result.error:
            return result
        authors = []
        date = None
        checked = False
        if result.matched:
            for name, value in result.value:
                if 'author' == name:
                    authors.append(value)
                elif 'date' == name:
                    # TODO: return error on duplicate date attribute
                    date = value
                elif 'checked' == name:
                    # TODO: return error on duplicate checked attribute
                    checked = True
                else:
                    raise RuntimeError(f'Unexpected link attribute type "{name}"')

        link = Link(
            modifier=modifier,
            title=title,
            url=url,
            authors=authors,
            date=date,
            checked=checked,
        )
        return ProductionResult(True, value=link)

    def general_link_directive(self) -> Matched[Tuple[str, str]] | ParserError:
        if not self.is_general_link_modifier():
            return MissingLinkModifierError(self.token)
        modifier = self.token.text
        self.next_token()

        if not self.is_data():
            return MissingDataError(self.token, 'link title')
        title = self.token.text
        self.next_token()

        return Matched((modifier, title))

    def author_directive(self) -> Matched[str] | NotMatched | ParserError:
        if not self.is_directive('author'):
            return NotMatched()
        self.next_token()

        if not self.is_data():
            return MissingDataError(self.token, 'author value')
        author = self.token.text
        self.next_token()

        return Matched(author)

    def date_directive(self) -> Matched[str] | NotMatched | ParserError:
        if not self.is_directive('date'):
            return NotMatched()
        self.next_token()

        if not self.is_data():
            return MissingDataError(self.token, 'date value')
        date = self.token.text
        self.next_token()

        return Matched(date)

    def checked_directive(self) -> Matched[bool] | NotMatched:
        if not self.is_directive('checked'):
            return NotMatched()
        self.next_token()
        return Matched(True)

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
