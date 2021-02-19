from dataclasses import dataclass
from enum import Enum, auto

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
    BLANK_LINE = auto()
    TEXT_LINE = auto()


@dataclass
class Token:
    type: TokenType
    text: str


modifiers = ['links', 'book']


def unescape(text: str) -> str:
    return text


def tokenize(source: str) -> Token:
    for line in source.splitlines():
        if 0 == len(line):
            yield Token(TokenType.BLANK_LINE, line)
        elif line.isspace():
            yield Token(TokenType.BLANK_LINE, line)
        elif '.' is line[0]:
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
            yield Token(TokenType.TEXT_LINE, unescape(line))


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
