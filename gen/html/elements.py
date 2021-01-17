from typing import Optional

from html.comment import Comment
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


class Body(Element):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='body', parent=parent, **kwargs)

    def omit_end_tag(self) -> bool:
        if self.next_sibling:
            return not isinstance(self.next_sibling, Comment)
        else:
            return True


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


class Em(Element):
    def __init__(
            self,
            text: str,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(name='em', parent=parent, **kwargs)
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
        super().__init__(name='h1', parent=parent, **kwargs)
        self.format = Format.COMPACT
        Text(text, parent=self)


class H2(Element):
    def __init__(self, text: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='h2', parent=parent, **kwargs)
        self.format = Format.COMPACT
        Text(text, parent=self)


class Head(Element):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='head', parent=parent, **kwargs)


class HTML(Element):
    def __init__(self, lang: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='html', parent=parent, **kwargs)
        self.attributes['lang'] = lang
        self.indent_children = False


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

    def omit_end_tag(self) -> bool:
        if self.next_sibling:
            return self.next_sibling.name in [
                'address', 'article', 'aside', 'blockquote', 'details', 'div',
                'dl', 'fieldset', 'figcaption', 'figure', 'footer', 'form',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hr', 'main',
                'nav', 'ol', 'p', 'pre', 'section', 'table', 'ul'
            ]
        elif self.parent:
            return self.parent.name not in [
                'a', 'audio', 'del', 'ins', 'map', 'noscript', 'video'
            ]
        else:
            return True


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
        super().__init__(name='strong', parent=parent, **kwargs)
        self.format = Format.INLINE
        Text(text, parent=self)


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
            class_names=class_names,
            parent=parent,
            **kwargs,
        )
        self.attributes['datetime'] = datetime
        self.format = Format.INLINE
        Text(datetime, parent=self)


class Title(Element):
    def __init__(self, title: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='title', parent=parent, **kwargs)
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
