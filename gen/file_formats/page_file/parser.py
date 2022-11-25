from dataclasses import dataclass
from typing import Optional, TypeVar, Generic, List, Tuple

from file_formats.page_file import PageFile, LinksSection, Link, BookLink
from .lexer import Token, TokenType, lexer


LINK_MODIFIERS = ['blog', 'docs', 'email', 'paper', 'podcast', 'repo', 'site']
PAGE_MODIFIERS = ['author', 'essay', 'links']


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


class InvalidModifierError(ParserError):
    def __init__(self, token: Token, modifiers: List[str]):
        self.modifiers = modifiers
        super().__init__(token, f'Expected one of these modifiers: {modifiers}')


class MissingDirectiveError(ParserError):
    def __init__(self, token: Token, directive: str):
        self.directive = directive
        super().__init__(token, f'Expected `.{directive}` directive')


class MissingDirectivesError(ParserError):
    def __init__(self, token: Token, directives: List[str]):
        self.directives = directives
        directives_list = ', '.join([
            f'.{directive}' for directive in directives
        ])
        super().__init__(token, f'Expected one of these directives: {directives_list}')


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

        page_directive = '.page' page_modifier DATA

        page_modifier = 'author' | 'essay' | 'links'

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

        general_link_modifier = 'blog' | 'docs' | 'email' | 'paper' | 'podcast' | 'repo' | 'site'
    """

    def __init__(self, source: str):
        self.lexer = lexer(source)
        self.token: Optional[Token] = None

    def parse(self) -> PageFile | ParserError:
        self.next_token()

        match self.page():
            case Matched(page):
                if self.token:
                    return UnexpectedTokenError(self.token)
                return page
            case ParserError() as e:
                return e

    def page(self) -> Matched[PageFile] | ParserError:
        match self.overview():
            case Matched((modifier, title, subtitle, notes)):
                pass
            case ParserError() as e:
                return e

        match self.sections():
            case Matched(sections):
                pass
            case NotMatched():
                sections = []
            case ParserError() as e:
                return e

        page = PageFile(
            modifier=modifier,
            title=title,
            subtitle=subtitle,
            notes=notes,
            sections=sections
        )
        return Matched(page)

    def overview(self) -> Matched[Tuple[str, str, Optional[str], List[str]]] | ParserError:
        match self.page_attributes():
            case Matched((modifier, title, subtitle)):
                pass
            case ParserError() as e:
                return e

        match self.paragraphs():
            case Matched(notes):
                pass
            case NotMatched():
                notes = []
            case ParserError() as e:
                return e

        return Matched((modifier, title, subtitle, notes))

    def page_attributes(self) -> Matched[Tuple[str, str, Optional[str]]] | ParserError:
        match self.page_directive():
            case Matched((modifier, title)):
                pass
            case ParserError() as e:
                return e

        match self.subtitle_directive():
            case Matched(subtitle):
                pass
            case NotMatched():
                subtitle = None
            case ParserError() as e:
                return e

        return Matched((modifier, title, subtitle))

    def page_directive(self) -> Matched[Tuple[str, str]] | ParserError:
        if not self.is_directive('page'):
            return MissingDirectiveError(self.token, 'page')
        self.next_token()

        if not self.is_in_modifier_list(PAGE_MODIFIERS):
            return InvalidModifierError(self.token, PAGE_MODIFIERS)
        modifier = self.token.text.strip()
        self.next_token()

        if not self.is_data():
            return MissingDataError(self.token, 'page title')
        title = self.token.text.strip()
        self.next_token()

        return Matched((modifier, title))

    def subtitle_directive(self) -> Matched[str] | NotMatched | ParserError:
        if not self.is_directive('subtitle'):
            return NotMatched()
        self.next_token()

        if not self.is_data():
            return MissingDataError(self.token, 'page subtitle')
        subtitle = self.token.text.strip()
        self.next_token()

        return Matched(subtitle)

    def paragraphs(self) -> Matched[List[str]] | NotMatched | ParserError:
        if not self.is_paragraph():
            return NotMatched()
        paragraph = self.token.text
        self.next_token()

        match self.paragraphs():
            case Matched(paragraphs):
                return Matched([paragraph] + paragraphs)
            case NotMatched():
                return Matched([paragraph])
            case ParserError() as e:
                return e

    def sections(self) -> Matched[List[LinksSection]] | NotMatched | ParserError:
        match self.section():
            case Matched(section):
                pass
            case NotMatched():
                return NotMatched()
            case ParserError() as e:
                return e

        match self.sections():
            case Matched(sections):
                return Matched([section] + sections)
            case NotMatched():
                return Matched([section])
            case ParserError() as e:
                return e

    def section(self) -> Matched[LinksSection] | NotMatched | ParserError:
        match self.section_directive():
            case Matched(title):
                pass
            case NotMatched():
                return NotMatched()
            case ParserError() as e:
                return e

        match self.paragraphs():
            case Matched(notes):
                pass
            case NotMatched():
                notes = []
            case ParserError() as e:
                return e

        match self.links():
            case Matched(links):
                pass
            case NotMatched():
                links = []
            case ParserError() as e:
                return e

        section = LinksSection(title=title, notes=notes, links=links)
        return Matched(section)

    def section_directive(self) -> Matched[str] | NotMatched | ParserError:
        if not self.is_directive('section'):
            return NotMatched()
        self.next_token()

        if not self.is_modifier('links'):
            return MissingModifierError(self.token, 'links')
        self.next_token()

        if not self.is_data():
            return MissingDataError(self.token, 'section title')
        title = self.token.text
        self.next_token()

        return Matched(title)

    def links(self) -> Matched[List[BookLink | Link]] | NotMatched | ParserError:
        match self.link():
            case Matched(link):
                pass
            case NotMatched():
                return NotMatched()
            case ParserError() as e:
                return e

        match self.links():
            case Matched(links):
                return Matched([link] + links)
            case NotMatched():
                return Matched([link])
            case ParserError() as e:
                return e

    def link(self) -> Matched[BookLink | Link] | NotMatched | ParserError:
        if not self.is_directive('link'):
            return NotMatched()
        self.next_token()

        for x_link in [self.book_link, self.general_link]:
            match x_link():
                case Matched() as m:
                    return m
                case NotMatched():
                    pass
                case ParserError() as e:
                    return e

        return InvalidModifierError(self.token, LINK_MODIFIERS)

    def book_link(self) -> Matched[BookLink] | NotMatched | ParserError:
        match self.book_link_directive():
            case Matched(title):
                pass
            case NotMatched():
                return NotMatched()
            case ParserError() as e:
                return e

        match self.book_locator():
            case Matched((asin, url)):
                pass
            case NotMatched():
                return MissingDirectivesError(self.token, ['url', 'asin'])
            case ParserError() as e:
                return e

        match self.link_attributes():
            case Matched(attributes):
                match self.validate_link_attributes(attributes):
                    case authors, date, checked:
                        pass
                    case ParserError() as e:
                        return e
            case NotMatched():
                authors, date, checked = [], None, False
            case ParserError() as e:
                return e

        link = BookLink(
            modifier='book',
            title=title,
            url=url,
            asin=asin,
            authors=authors,
            date=date,
            checked=checked,
        )
        return Matched(link)

    def book_link_directive(self) -> Matched[str] | NotMatched | ParserError:
        if not self.is_modifier('book'):
            return NotMatched()
        self.next_token()

        if not self.is_data():
            return MissingDataError(self.token, 'link title')
        title = self.token.text
        self.next_token()

        return Matched(title)

    def book_locator(self) -> Matched[Tuple[Optional[str], Optional[str]]] | NotMatched | ParserError:
        match self.asin_directive():
            case Matched(asin):
                match self.url_directive():
                    case Matched(url):
                        return Matched((asin, url))
                    case NotMatched():
                        return Matched((asin, None))
                    case ParserError() as e:
                        return e
            case NotMatched():
                pass
            case ParserError() as e:
                return e

        match self.url_directive():
            case Matched(url):
                match self.asin_directive():
                    case Matched(asin):
                        return Matched((asin, url))
                    case NotMatched():
                        return Matched((None, url))
                    case ParserError() as e:
                        return e
            case NotMatched():
                return NotMatched()
            case ParserError() as e:
                return e

    def url_directive(self) -> Matched[str] | NotMatched | ParserError:
        if not self.is_directive('url'):
            return NotMatched()
        self.next_token()

        if not self.is_data():
            return MissingDataError(self.token, 'URL address')
        url = self.token.text
        self.next_token()

        return Matched(url)

    def asin_directive(self) -> Matched[str] | NotMatched | ParserError:
        if not self.is_directive('asin'):
            return NotMatched()
        self.next_token()

        if not self.is_data():
            return MissingDataError(self.token, 'ASIN')
        asin = self.token.text
        self.next_token()

        return Matched(asin)

    def link_attributes(self) -> Matched[List[Tuple[str, str]]] | NotMatched | ParserError:
        match self.link_attribute():
            case Matched(attribute):
                pass
            case NotMatched():
                return NotMatched()
            case ParserError() as e:
                return e

        match self.link_attributes():
            case Matched(attributes):
                return Matched([attribute] + attributes)
            case NotMatched():
                return Matched([attribute])
            case ParserError() as e:
                return e

    def link_attribute(self) -> Matched[Tuple[str, str]] | NotMatched | ParserError:
        match self.author_directive():
            case Matched(author):
                return Matched(('author', author))
            case NotMatched():
                pass
            case ParserError() as e:
                return e

        match self.date_directive():
            case Matched(date):
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

    def general_link(self) -> Matched[Link] | NotMatched | ParserError:
        match self.general_link_directive():
            case Matched((modifier, title)):
                pass
            case NotMatched():
                return NotMatched()
            case ParserError() as e:
                return e

        match self.url_directive():
            case Matched(url):
                pass
            case NotMatched():
                return MissingDirectiveError(self.token, 'url')
            case ParserError() as e:
                return e

        match self.link_attributes():
            case Matched(attributes):
                match self.validate_link_attributes(attributes):
                    case authors, date, checked:
                        pass
                    case ParserError() as e:
                        return e
            case NotMatched():
                authors, date, checked = [], None, False
            case ParserError() as e:
                return e

        link = Link(
            modifier=modifier,
            title=title,
            url=url,
            authors=authors,
            date=date,
            checked=checked,
        )
        return Matched(link)

    def general_link_directive(self) -> Matched[Tuple[str, str]] | NotMatched | ParserError:
        if not self.is_in_modifier_list(LINK_MODIFIERS):
            return NotMatched()
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

    def is_modifier(self, modifier: str) -> bool:
        return (
                self.token
                and TokenType.MODIFIER == self.token.type
                and modifier == self.token.text
        )

    def is_in_modifier_list(self, modifiers: List[str]) -> bool:
        return (
                self.token
                and TokenType.MODIFIER == self.token.type
                and self.token.text in modifiers
        )

    def is_paragraph(self) -> bool:
        return (
                self.token
                and TokenType.PARAGRAPH == self.token.type
        )

    def validate_link_attributes(self, attributes) -> Tuple[List[str], Optional[str], bool] | ParserError:
        authors = []
        date = None
        checked = False
        for name, value in attributes:
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
        return authors, date, checked
