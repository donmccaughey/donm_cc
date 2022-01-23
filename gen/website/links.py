from typing import Optional, Sequence

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
    with Li(class_names=[modifier]):
        A(href=href, text=title, class_names=['title'])
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
        href: Optional[str] = None,
        asin: Optional[str] = None,
        authors: Sequence[str] = (),
        date: Optional[str] = None,
        checked: bool = False
):
    link(
        modifier='book',
        title=title,
        href=href,
        authors=authors,
        date=date,
        checked=checked,
    )
