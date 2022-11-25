from typing import Optional, Sequence

from markdown import inline_markdown_to_markup
from markup import Li, A, Text, Span, Time


def join_authors(authors: list[str]) -> str:
    if 1 == len(authors):
        return authors[0]
    else:
        last = authors[-2] + ' and ' + authors[-1]
        authors[-2:] = [last]
        return ', '.join(authors)


def link(
        modifier: str,
        title: str,
        href: str,
        authors: Sequence[str] = (),
        date: Optional[str] = None,
        checked: bool = False
):
    with Li():
        with A(href=href, class_names=['title']):
            inline_markdown_to_markup(title)
        if authors:
            Text(', ')
            Span(class_names=['authors'], text=join_authors(list(authors)))
        if date:
            Text(', ')
            Time(datetime=date)
        if checked:
            Text(' ✓')


def book(
        title: str,
        asin: Optional[str] = None,
        olw: Optional[str] = None,
        url: Optional[str] = None,
        authors: Sequence[str] = (),
        date: Optional[str] = None,
        checked: bool = False
):
    assert(asin or olw or url)
    if url:
        href = url
    elif olw:
        href = f'https://openlibrary.org/works/{olw}'
    else:
        href = f'https://www.amazon.com/dp/{asin}'
    link(
        modifier='book',
        title=title,
        href=href,
        authors=authors,
        date=date,
        checked=checked,
    )
