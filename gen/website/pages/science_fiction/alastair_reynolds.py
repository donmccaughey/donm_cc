from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterator, Union, Optional

from markup import Section, H1, P, Ul, A, Text
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

.link book Chasm City
.url https://www.amazon.com/gp/product/B000OIZUH6
.date 2001
.checked

.link book Diamond Dogs, Turquoise Days
.url https://www.amazon.com/gp/product/B001JJWICY
.date 2002
.checked

.link book Redemption Ark
.url https://www.amazon.com/gp/product/B001LFDABO
.date 2002
.checked

.link book Absolution Gap
.url https://www.amazon.com/gp/product/B001ODO61G
.date 2003
.checked

.link book Galactic North
.url https://www.amazon.com/gp/product/B0017SWQJW
.date 2006

.link book The Prefect / Aurora Rising 
.url https://www.amazon.com/gp/product/B0015DYJY4
.date 2007
.checked

.link book Elysium Fire
.url https://www.amazon.com/gp/product/B073P43TMS
.date 2018
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

.link book Poseidon's Wake
.url https://www.amazon.com/gp/product/B00X5937LW
.date 2015
.checked


.section links Revenger

.link book Revenger
.url https://www.amazon.com/gp/product/B01LXW2IUQ
.date 2016
.checked

.link book Shadow Captain
.url https://www.amazon.com/gp/product/B07CWQN8FQ
.date 2019

.link book Bone Silence
.url https://www.amazon.com/gp/product/B0819W4456
.date 2020

.section links Merlin

<a href=http://approachingpavonis.blogspot.com/2016/10/new-merlin-story-iron-tactician.html>There are four Merlin stories to date, ...</a>

.link book Hideaway
.url https://www.goodreads.com/book/show/34793859-hideaway
.date 2000

.link book Minla's Flowers (included in <em>Zima Blue</em>)
.url https://www.amazon.com/gp/product/B00GVG07DC
.date 2009
.checked

.link book The Iron Tactician
.url https://www.amazon.com/Iron-Tactician-Alastair-Reynolds-ebook/dp/B01M2B9P7V
.date 2016

.link book Merlin's Gun
.url https://www.amazon.com/Mammoth-Books-presents-Merlins-Gun-ebook/dp/B00OGUTTEI
.date 2012
.checked


.section links House of Suns

.link book Thousandth Night
.url https://www.amazon.com/Thousandth-Night-Alastair-Reynolds-ebook/dp/B00C89ORWI
.date 2013

.link book House of Suns
.url https://www.amazon.com/gp/product/B002AKPECW
.date 2008
.checked


.section links Other Stories

.link book Century Rain
.url https://www.amazon.com/gp/product/B0010SB6OK
.date 2004
.checked

.link book Pushing Ice
.url https://www.amazon.com/gp/product/B00NW2Z04E
.date 2005
.checked

.link book Terminal World
.url https://www.amazon.com/gp/product/B01K3LNPCK
.date 2009

.link book Troika
.url https://www.amazon.com/gp/product/B00C89K574
.date 2010
.checked

.link book Sleepover
.url https://www.amazon.com/gp/product/B00OGUTOE8
.date 2010

.link book Slow Bullets
.url https://www.amazon.com/gp/product/B00WGX4KT6
.date 2015
.checked

.link book Permafrost
.url https://www.amazon.com/gp/product/B07HF26D1H
.date 2019


.section links Collections

Reynolds' short stories are like small bite-sized versions of his
novels.  Notably, the stories <em>Zima Blue</em> and <em>Beyond the Aquila Rift</em>
come to life in episodes of the animated series
<a href=https://www.netflix.com/title/80174608>Love, Death & Robots</a>.

.link book Zima Blue
.url https://www.amazon.com/gp/product/B00GVG07DC
.date 2006
.checked

.link book The Six Directions of Space
.url https://www.amazon.com/Six-Directions-Space-Alastair-Reynolds-ebook/dp/B00C89JZCA
.date 2008

.link book Deep Navigation
.url https://www.amazon.com/gp/product/B00XT0V0DY
.date 2010

.link book Beyond the Aquila Rift
.url https://www.amazon.com/gp/product/B01FE7KJ2C
.date 2016
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


def alastair_reynolds():
    parser = Parser(tokenize(source))
    if not parser.parse():
        raise parser.error
    parser.links_page.build()
