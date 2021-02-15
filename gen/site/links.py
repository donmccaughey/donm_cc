from typing import Optional

from markup import Li, A, Text, Span, Time


def link(
        type: str,
        title: str,
        href: str,
        authors: Optional[str] = None,
        date: Optional[str] = None,
        checked: bool = False
):
    with Li(class_names=[type]):
        A(href=href, text=title, class_names=['title'])
        if authors:
            Text(', ')
            Span(class_names=['authors'], text=authors)
        if date:
            Text(', ')
            Time(datetime=date)
        if checked:
            Text(' ✓')


def book(
        title: str,
        href: str,
        authors: Optional[str] = None,
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
