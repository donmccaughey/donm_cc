from typing import Optional

from tags.element import Element, ElementType
from tags.node import Node
from tags.text import Text


class Body(Element):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='body',
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
            parent=parent,
            **kwargs,
        )
        pass


class HTML(Element):
    def __init__(self, lang: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='html',
            indent_children=False,
            parent=parent,
            **kwargs,
        )
        self.attributes['lang'] = lang


class Link(Element):
    def __init__(
            self,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name='link',
            element_type=ElementType.EMPTY,
            parent=parent,
            **kwargs,
        )
        pass


class Meta(Element):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='meta',
            element_type=ElementType.EMPTY,
            parent=parent,
            **kwargs,
        )
        pass


class MetaCharset(Meta):
    def __init__(
            self,
            charset: str,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(parent=parent, **kwargs)
        self.attributes['charset'] = charset


class MetaViewport(Meta):
    def __init__(
            self,
            initial_scale: str,
            width: str,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(parent=parent, **kwargs)
        self.attributes['name'] = 'viewport'
        self.attributes['content'] = f'initial-scale={initial_scale}, width={width}'


class Nav(Element):
    def __init__(
            self,
            class_names: Optional[list[str]],
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='nav',
            class_names=class_names,
            parent=parent,
            **kwargs,
        )
        pass


class Stylesheet(Link):
    def __init__(self, href: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.attributes['rel'] = 'stylesheet'
        self.attributes['href'] = href


class Title(Element):
    def __init__(
            self,
            title: Optional[str] = None,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name='title',
            element_type=ElementType.COMPACT,
            parent=parent,
            **kwargs,
        )
        if title:
            Text(title, parent=self)
