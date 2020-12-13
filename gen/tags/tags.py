from typing import Optional

from tags.element import Element, ElementType
from tags.node import Node
from tags.text import Text


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
            element_type=ElementType.COMPACT if text else ElementType.CONTAINER,
            parent=parent,
            **kwargs,
        )
        self.attributes['href'] = href
        if text:
            Text(text, parent=self)


class Body(Element):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='body', parent=parent, **kwargs)
        pass


class Br(Element):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='br',
            element_type=ElementType.EMPTY,
            parent=parent,
            **kwargs,
        )
        pass


class Div(Element):
    def __init__(
            self,
            id: Optional[str] = None,
            class_names: Optional[list[str]] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='div',
            id=id,
            class_names=class_names,
            parent=parent,
            **kwargs,
        )
        pass


class Em(Element):
    def __init__(
            self,
            text: str,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='em',
            element_type=ElementType.COMPACT,
            parent=parent,
            **kwargs,
        )
        Text(text, parent=self)


class H1(Element):
    def __init__(self, text: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='h1',
            element_type=ElementType.COMPACT,
            parent=parent,
            **kwargs,
        )
        Text(text, parent=self)


class Head(Element):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='head', parent=parent, **kwargs)
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


class Img(Element):
    def __init__(
            self,
            src: str,
            alt: str,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='img',
            element_type=ElementType.EMPTY,
            parent=parent,
            **kwargs,
        )
        self.attributes['src'] = src
        self.attributes['alt'] = alt


class Link(Element):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
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
    def __init__(self, charset: str, parent: Optional[Node] = None, **kwargs):
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
            class_names: Optional[list[str]] = None,
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


class P(Element):
    def __init__(
            self,
            class_names: Optional[list[str]] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='p',
            class_names=class_names,
            parent=parent,
            **kwargs,
        )
        pass


class Section(Element):
    def __init__(
            self,
            class_names: Optional[list[str]] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='section',
            class_names=class_names,
            parent=parent,
            **kwargs,
        )
        pass


class Span(Element):
    def __init__(
            self,
            text: str,
            class_names: Optional[list[str]] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='span',
            element_type=ElementType.COMPACT,
            class_names=class_names,
            parent=parent,
            **kwargs,
        )
        Text(text, parent=self)


class Strong(Element):
    def __init__(
            self,
            text: str,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='strong',
            element_type=ElementType.COMPACT,
            parent=parent,
            **kwargs,
        )
        Text(text, parent=self)


class Stylesheet(Link):
    def __init__(self, href: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.attributes['rel'] = 'stylesheet'
        self.attributes['href'] = href


class Time(Element):
    def __init__(
            self,
            datetime: str,
            class_names: Optional[list[str]] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='time',
            element_type=ElementType.COMPACT,
            class_names=class_names,
            parent=parent,
            **kwargs,
        )
        self.attributes['datetime'] = datetime
        Text(datetime, parent=self)


class Title(Element):
    def __init__(self, title: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='title',
            element_type=ElementType.COMPACT,
            parent=parent,
            **kwargs,
        )
        Text(title, parent=self)
