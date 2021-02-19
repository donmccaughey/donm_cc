from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterator

from markup import Section, H1, P, Ul, A, Text
from resources import Page
from website.links import link as build_link


@dataclass
class Link:
    type: str
    title: str
    link: str
    date: str
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


source = """
.page links Alastair Reynolds

Reynolds is an astrophysicist turned writer with a nack for
creating trippy, mind-bending stories.

.section links Revelation Space

<em>Revelation Space</em> is the gateway drug that got me hooked
on Reynolds' strange vision of the future.  It forms
a loosely connected trilogy with <em>Redemption Ark</em> (featuring
a riveting near-light-speed chase between the stars spanning decades) and 
<em>Absolution Gap</em> (with a virus-induced religious cult, moving cathedrals
and a vanishing gas giant). 

<em>Aurora Rising</em> and <em>Elysium Fire</em> form the
<a href=http://approachingpavonis.blogspot.com/2017/07/elysium-fire-and-new-title-for-prefect.html>Prefect
Dreyfuss Emergency</a> sub-series.  They're police procedurals
set in the Glitter Band, a swarm of thousands of orbital habitats.

.link book Revelation Space
.url https://www.amazon.com/gp/product/B001QL5MAA
.date 2000
.checked


.section links Poseidon's Children

.link book Blue Remembered Earth
.url https://www.amazon.com/gp/product/B005ZOCF5E
.date 2012
.checked

.link book On the Steel Breeze
.url https://www.amazon.com/gp/product/B00H2V6IN8
.date 2013
.checked


.section links Revenger

.link book Revenger
.url https://www.amazon.com/gp/product/B01LXW2IUQ
.date 2016
.checked

.link book Shadow Captain
.url https://www.amazon.com/gp/product/B07CWQN8FQ
.date 2019
"""


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


def tokenize(source: str) -> Token:
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
                    yield Token(TokenType.DATA, unescape(parts[2]))
                else:
                    data = parts[1] + ' ' + parts[2]
                    yield Token(TokenType.DATA, unescape(data))
        else:
            paragraph.append(line)
    if paragraph:
        yield Token(TokenType.PARAGRAPH, '\n'.join(paragraph))


class ParserError(RuntimeError):
    def __init__(self, token: Token, message: str):
        super().__init__(message)


"""
grammar:
    
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
class Parser:
    def __init__(self, lexer: Iterator[Token]):
        self.lexer = lexer
        self.token = None
        self.error = None

    def start(self) -> bool:
        self.next_token()
        # TODO: detect incomplete parse
        parsed = self.page()
        if not parsed:
            print(self.error)
        return parsed

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
        print(f'links page {self.token.text}')
        self.next_token()
        return True

    def paragraphs(self) -> bool:
        if not self.is_paragraph():
            self.error = ParserError(self.token, 'Expected a paragraph')
            return False
        print(f'paragraph "{self.token.text[:20]}..."')
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
        print(f'links section {self.token.text}')
        self.next_token()
        return True

    def links(self) -> bool:
        if not self.link():
            return False
        self.link()
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
        print(f'book link for {self.token.text}')
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
        print(f'link URL {self.token.text}')
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
        print(f'link date {self.token.text}')
        self.next_token()
        return True

    def checked_directive(self) -> bool:
        if not self.is_directive('checked'):
            self.error = ParserError(self.token, 'Expected .checked directive')
            return False
        print('link checked')
        self.next_token()
        return True


page = LinksPage(
    title='Alastair Reynolds',
    notes=[
        """
            Reynolds is an astrophysicist turned writer with a nack for
            creating trippy, mind-bending stories.
        """
        ],
    sections=[
        LinksSection(
            title='Revelation Space',
            notes=[
                """
                    <em>Revelation Space</em> is the gateway drug that got me hooked
                    on Reynolds' strange vision of the future.  It forms
                    a loosely connected trilogy with <em>Redemption Ark</em> (featuring
                    a riveting near-light-speed chase between the stars spanning decades) and 
                    <em>Absolution Gap</em> (with a virus-induced religious cult, moving cathedrals
                    and a vanishing gas giant). 
                """,
                """
                    <em>Aurora Rising</em> and <em>Elysium Fire</em> form the
                    <a href=http://approachingpavonis.blogspot.com/2017/07/elysium-fire-and-new-title-for-prefect.html>Prefect
                    Dreyfuss Emergency</a> sub-series.  They're police procedurals
                    set in the Glitter Band, a swarm of thousands of orbital habitats.
                """,
            ],
            links=[
                Link(
                    type='book',
                    title='Revelation Space',
                    link='https://www.amazon.com/gp/product/B001QL5MAA',
                    date='2000',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='Chasm City',
                    link='https://www.amazon.com/gp/product/B000OIZUH6',
                    date='2001',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='Diamond Dogs, Turquoise Days',
                    link='https://www.amazon.com/gp/product/B001JJWICY',
                    date='2002',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='Redemption Ark',
                    link='https://www.amazon.com/gp/product/B001LFDABO',
                    date='2002',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='Absolution Gap',
                    link='https://www.amazon.com/gp/product/B001ODO61G',
                    date='2003',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='Galactic North',
                    link='https://www.amazon.com/gp/product/B0017SWQJW',
                    date='2006',
                    checked=False,
                ),
                Link(
                    type='book',
                    title='The Prefect / Aurora Rising',
                    link='https://www.amazon.com/gp/product/B0015DYJY4',
                    date='2007',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='Elysium Fire',
                    link='https://www.amazon.com/gp/product/B073P43TMS',
                    date='2018',
                    checked=True,
                ),
            ]
        ),
        LinksSection(
            title="Poseidon's Children",
            notes=[],
            links=[
                Link(
                    type='book',
                    title='Blue Remembered Earth',
                    link='https://www.amazon.com/gp/product/B005ZOCF5E',
                    date='2012',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='On the Steel Breeze',
                    link='https://www.amazon.com/gp/product/B00H2V6IN8',
                    date='2013',
                    checked=True,
                ),
                Link(
                    type='book',
                    title="Poseidon's Wake",
                    link='https://www.amazon.com/gp/product/B00X5937LW',
                    date='2015',
                    checked=True,
                ),
            ]
        ),
        LinksSection(
            title='Revenger',
            notes=[],
            links=[
                Link(
                    type='book',
                    title='Revenger',
                    link='https://www.amazon.com/gp/product/B01LXW2IUQ',
                    date='2016',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='Shadow Captain',
                    link='https://www.amazon.com/gp/product/B07CWQN8FQ',
                    date='2019',
                    checked=False,
                ),
                Link(
                    type='book',
                    title='Bone Silence',
                    link='https://www.amazon.com/gp/product/B0819W4456',
                    date='2020',
                    checked=False,
                ),
            ]
        ),
        LinksSection(
            title='Merlin',
            notes=[
                """
                    <a href=http://approachingpavonis.blogspot.com/2016/10/new-merlin-story-iron-tactician.html>There are four Merlin stories to date, ...</a>
                """
            ],
            links=[
                Link(
                    type='book',
                    title='Hideaway',
                    link='https://www.goodreads.com/book/show/34793859-hideaway',
                    date='2000',
                    checked=False,
                ),
                Link(
                    type='book',
                    title="Minla's Flowers (included in <em>Zima Blue</em>)",
                    link='https://www.amazon.com/gp/product/B00GVG07DC',
                    date='2009',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='The Iron Tactician',
                    link='https://www.amazon.com/Iron-Tactician-Alastair-Reynolds-ebook/dp/B01M2B9P7V',
                    date='2016',
                    checked=False,
                ),
                Link(
                    type='book',
                    title="Merlin's Gun",
                    link='https://www.amazon.com/Mammoth-Books-presents-Merlins-Gun-ebook/dp/B00OGUTTEI',
                    date='2012',
                    checked=True,
                ),
            ]
        ),
        LinksSection(
            title='House of Suns',
            notes=[],
            links=[
                Link(
                    type='book',
                    title='Thousandth Night',
                    link='https://www.amazon.com/Thousandth-Night-Alastair-Reynolds-ebook/dp/B00C89ORWI',
                    date='2013',
                    checked=False,
                ),
                Link(
                    type='book',
                    title='House of Suns',
                    link='https://www.amazon.com/gp/product/B002AKPECW',
                    date='2008',
                    checked=True,
                ),
            ]
        ),
        LinksSection(
            title='Other Stories',
            notes=[],
            links=[
                Link(
                    type='book',
                    title='Century Rain',
                    link='https://www.amazon.com/gp/product/B0010SB6OK',
                    date='2004',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='Pushing Ice',
                    link='https://www.amazon.com/gp/product/B00NW2Z04E',
                    date='2005',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='Terminal World',
                    link='https://www.amazon.com/gp/product/B01K3LNPCK',
                    date='2009',
                    checked=False,
                ),
                Link(
                    type='book',
                    title='Troika',
                    link='https://www.amazon.com/gp/product/B00C89K574',
                    date='2010',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='Sleepover',
                    link='https://www.amazon.com/gp/product/B00OGUTOE8',
                    date='2010',
                    checked=False,
                ),
                Link(
                    type='book',
                    title='Slow Bullets',
                    link='https://www.amazon.com/gp/product/B00WGX4KT6',
                    date='2015',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='Permafrost',
                    link='https://www.amazon.com/gp/product/B07HF26D1H',
                    date='2019',
                    checked=False,
                ),
            ]
        ),
        LinksSection(
            title='Collections',
            notes=[
                """
                    Reynolds' short stories are like small bite-sized versions of his
                    novels.  Notably, the stories <em>Zima Blue</em> and <em>Beyond the Aquila Rift</em>
                    come to life in episodes of the animated series
                    <a href=https://www.netflix.com/title/80174608>Love, Death & Robots</a>.
                """
            ],
            links=[
                Link(
                    type='book',
                    title='Zima Blue',
                    link='https://www.amazon.com/gp/product/B00GVG07DC',
                    date='2006',
                    checked=True,
                ),
                Link(
                    type='book',
                    title='The Six Directions of Space',
                    link='https://www.amazon.com/Six-Directions-Space-Alastair-Reynolds-ebook/dp/B00C89JZCA',
                    date='2008',
                    checked=False,
                ),
                Link(
                    type='book',
                    title='Deep Navigation',
                    link='https://www.amazon.com/gp/product/B00XT0V0DY',
                    date='2010',
                    checked=False,
                ),
                Link(
                    type='book',
                    title='Beyond the Aquila Rift',
                    link='https://www.amazon.com/gp/product/B01FE7KJ2C',
                    date='2016',
                    checked=False,
                ),
            ]
        )
    ]
)


def alastair_reynolds():
    page.build()
