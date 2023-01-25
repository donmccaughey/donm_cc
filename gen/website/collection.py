from urllib.parse import urlsplit
from typing import Optional

from markup import Li, A, Strong, Em, Text


def item(
        title: str,
        href: str,
        subtitle: Optional[str] = None,
):
    with Li(class_names=['item']):
        with A(href=href) as a:
            scheme, netloc, *_ = urlsplit(href)
            if scheme or netloc:
                a.attributes['rel'] = 'noreferrer'
                a.attributes['target'] = '_blank'
            Strong(title)
            if subtitle:
                Text(': ')
                Em(subtitle)
