from typing import Optional

from markup import Li, A, Img, Strong, Br, Em


def item(
        title: str,
        href: str,
        subtitle: Optional[str] = None,
        favicon: Optional[str] = None,
        external: bool = False,
):
    class_names = ['item'] + (['external'] if external else [])
    with Li(class_names=class_names):
        with A(href=href):
            if favicon:
                Img(class_names=['favicon'], src=favicon, alt=f'{title} icon')
            Strong(title)
            if subtitle:
                Br()
                Em(subtitle)
