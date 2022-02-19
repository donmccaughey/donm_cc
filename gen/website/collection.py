from typing import Optional

from markup import Li, A, Img, Strong, Br, Em, Text


def item(
        title: str,
        href: str,
        subtitle: Optional[str] = None,
):
    with Li(class_names=['item']):
        with A(href=href):
            Strong(title)
            if subtitle:
                Text(': ')
                Em(subtitle)
