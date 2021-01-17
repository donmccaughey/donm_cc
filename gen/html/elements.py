from typing import Optional
from html.element import Element, ElementType
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
            element_type=ElementType.COMPACT if text else ElementType.CONTAINER,
            parent=parent,
            **kwargs,
        )
        self.attributes['href'] = href
        self.format = Format.INLINE
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
        self.format = Format.INLINE
        self.has_end_tag = False


class Button(Element):
    def __init__(
            self,
            text: str,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='button',
            element_type=ElementType.COMPACT,
            parent=parent,
            **kwargs,
        )
        self.format = Format.INLINE
        Text(text, parent=self)


class Code(Element):
    def __init__(
            self,
            text: str,
            class_names: Optional[list[str]] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='code',
            element_type=ElementType.COMPACT,
            class_names=class_names,
            parent=parent,
            **kwargs,
        )
        self.format = Format.INLINE
        Text(text, parent=self)


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
        self.format = Format.INLINE
        Text(text, parent=self)


class Form(Element):
    def __init__(
            self,
            action: str,
            method: Optional[str] = 'POST',
            class_names: Optional[list[str]] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='form',
            class_names=class_names,
            parent=parent,
            **kwargs,
        )
        self.attributes['action'] = action
        self.attributes['method'] = method


class H1(Element):
    def __init__(self, text: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='h1',
            element_type=ElementType.COMPACT,
            parent=parent,
            **kwargs,
        )
        self.format = Format.COMPACT
        Text(text, parent=self)


class H2(Element):
    def __init__(self, text: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='h2',
            element_type=ElementType.COMPACT,
            parent=parent,
            **kwargs,
        )
        self.format = Format.COMPACT
        Text(text, parent=self)


class Head(Element):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='head', parent=parent, **kwargs)
        pass


class HTML(Element):
    def __init__(self, lang: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='html',
            parent=parent,
            **kwargs,
        )
        self.attributes['lang'] = lang
        self.indent_children = False


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
        self.format = Format.INLINE
        self.has_end_tag = False


class Input(Element):
    def __init__(
            self,
            id: str,
            name: Optional[str] = None,
            type: Optional[str] = None,
            value: Optional[str] = None,
            checked: Optional[bool] = False,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name='input',
            element_type=ElementType.EMPTY,
            parent=parent,
            **kwargs,
        )
        self.attributes['id'] = id
        self.attributes['name'] = name if name else id
        if type:
            self.attributes['type'] = type
        if value:
            self.attributes['value'] = value
        if checked:
            self.attributes['checked'] = None
        self.format = Format.COMPACT
        self.has_end_tag = False


class Link(Element):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='link',
            element_type=ElementType.EMPTY,
            parent=parent,
            **kwargs,
        )
        self.has_end_tag = False


class Label(Element):
    def __init__(
            self,
            text: str,
            for_id: Optional[str] = None,
            parent: Optional[Node] = None,
            **kwargs
    ):
        super().__init__(
            name='label',
            element_type=ElementType.COMPACT,
            parent=parent,
            **kwargs,
        )
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
        pass


class Meta(Element):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='meta',
            element_type=ElementType.EMPTY,
            parent=parent,
            **kwargs,
        )
        self.has_end_tag = False


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
            text: Optional[str] = None,
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
        if text:
            Text(text, parent=self)


class Script(Element):
    def __init__(
            self,
            src: str,
            charset: Optional[str] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='script',
            element_type=ElementType.COMPACT,
            parent=parent,
            **kwargs,
        )
        if charset:
            self.attributes['charset'] = charset
        self.attributes['src'] = src
        self.attributes['type'] = 'text/javascript'
        self.format = Format.COMPACT # TODO: script containing code should be .BLOCK


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
        self.format = Format.INLINE
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
        self.format = Format.INLINE
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
        self.format = Format.INLINE
        Text(datetime, parent=self)


class Title(Element):
    def __init__(self, title: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(
            name='title',
            element_type=ElementType.COMPACT,
            parent=parent,
            **kwargs,
        )
        self.format = Format.COMPACT
        Text(title, parent=self)


class Ul(Element):
    def __init__(
            self,
            id: Optional[str] = None,
            class_names: Optional[list[str]] = None,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(
            name='ul',
            id=id,
            class_names=class_names,
            parent=parent,
            **kwargs,
        )
        pass
