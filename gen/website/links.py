from typing import Optional, List

from markup import Li, A, Text, Span, Time


def join_authors(authors: List[str]) -> str:
    if 1 == len(authors):
        return authors[0]
    else:
        last = authors[-2] + ' and ' + authors[-1]
        authors[-2:] = [last]
        return ', '.join(authors)


def link(
        type: str,
        title: str,
        href: str,
        authors: List[str] = [],
        date: Optional[str] = None,
        checked: bool = False
):
    with Li(class_names=[type]):
        A(href=href, text=title, class_names=['title'])
        if authors:
            Text(', ')
            Span(class_names=['authors'], text=join_authors(authors))
        if date:
            Text(', ')
            Time(datetime=date)
        if checked:
            Text(' ✓')


def book(
        title: str,
        href: str,
        authors: List[str] = [],
        date: Optional[str] = None,
        checked: bool = False
):
    link(
        type='book',
        title=title,
        href=href,
        authors=authors,
        date=date,
        checked=checked,
    )
