from typing import Optional

from tags.element import Element, ElementType
from tags.node import Node
from tags.text import Text


class Body(Element):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='body',
            attributes=None,
            parent=parent,
            **kwargs,
        )
        pass


class H1(Element):
    def __init__(
            self,
            text: Optional[str] = None,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name='h1',
            attributes=None,
            element_type=ElementType.COMPACT,
            parent=parent,
            **kwargs,
        )
        if text:
            Text(text, parent=self)


class Head(Element):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='head',
            attributes=None,
            parent=parent,
            **kwargs,
        )
        pass


class HTML(Element):
    def __init__(self, lang: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='html',
            attributes={'lang': lang},
            indent_children=False,
            parent=parent,
            **kwargs,
        )
        pass


class Link(Element):
    def __init__(
            self,
            attributes: dict[str, str],
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name='link',
            attributes=attributes,
            element_type=ElementType.EMPTY,
            parent=parent,
            **kwargs,
        )
        pass


class Meta(Element):
    def __init__(
            self,
            attributes: dict[str, str],
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name='meta',
            attributes=attributes,
            element_type=ElementType.EMPTY,
            parent=parent,
            **kwargs,
        )
        pass


class Title(Element):
    def __init__(
            self,
            title: Optional[str] = None,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name='title',
            attributes=None,
            element_type=ElementType.COMPACT,
            parent=parent,
            **kwargs,
        )
        if title:
            Text(title, parent=self)
