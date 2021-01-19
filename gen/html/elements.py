from typing import Optional

from html.element import Element
from html.node import Node
from html.format import Format
from html.text import Text


def as_block(element: Element) -> Element:
    element.format = Format.BLOCK
    return element


def as_compact(element: Element) -> Element:
    element.format = Format.COMPACT
    return element


class A(Element):
    def __init__(
            self,
            href: str,
            text: Optional[str] = None,
            class_names: Optional[list[str]] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='a',
            class_names=class_names,
            parent=parent,
            **kwargs,
        )
        self.attributes['href'] = href
        self.format = Format.INLINE
        if text:
            Text(text, parent=self)


class Button(Element):
    def __init__(
            self,
            text: str,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(name='button', parent=parent, **kwargs)
        self.format = Format.INLINE
        Text(text, parent=self)


class H1(Element):
    def __init__(self, text: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='h1', parent=parent, **kwargs)
        self.format = Format.COMPACT
        Text(text, parent=self)


class H2(Element):
    def __init__(self, text: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='h2', parent=parent, **kwargs)
        self.format = Format.COMPACT
        Text(text, parent=self)


class Label(Element):
    def __init__(
            self,
            text: str,
            for_id: Optional[str] = None,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(name='label', parent=parent, **kwargs)
        self.format = Format.COMPACT
        if for_id:
            self.attributes['for'] = for_id
        Text(text, parent=self)


class Li(Element):
    def __init__(
            self,
            id: Optional[str] = None,
            class_names: Optional[list[str]] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='li',
            id=id,
            class_names=class_names,
            parent=parent,
            **kwargs,
        )


class Script(Element):
    def __init__(
            self,
            src: str,
            charset: Optional[str] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(name='script', parent=parent, **kwargs)
        if charset:
            self.attributes['charset'] = charset
        self.attributes['src'] = src
        self.attributes['type'] = 'text/javascript'
        self.format = Format.COMPACT # TODO: script containing code should be .BLOCK


class Title(Element):
    def __init__(self, title: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='title', parent=parent, **kwargs)
        self.format = Format.COMPACT
        Text(title, parent=self)
