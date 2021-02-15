from typing import Optional, List

from markup import Text
from markup.element import Element
from markup.node import Node
from markup.wrap import wrap_tokens


class InlineElement(Element):
    '''
    https://www.w3.org/TR/html52/dom.html#phrasing-content-2
    TODO: validate that inline elements only contain permissible children
    '''
    def __init__(self, name: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name=name, parent=parent, **kwargs)

    def markup(self, width: int) -> str:
        wrapped = wrap_tokens(self.tokens(), width)
        return ''.join(wrapped)

    def tokens(self) -> List[str]:
        tokens = [self.start_tag()]
        for child in self.children:
            tokens += child.tokens()
        tokens += [self.end_tag()]
        return tokens


class A(InlineElement):
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
        if text:
            Text(text, parent=self)


class Code(InlineElement):
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
        Text(text, parent=self)


class Em(InlineElement):
    def __init__(
            self,
            text: str,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(name='em', parent=parent, **kwargs)
        Text(text, parent=self)


class Span(InlineElement):
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
        Text(text, parent=self)


class Strong(InlineElement):
    def __init__(
            self,
            text: str,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(name='strong', parent=parent, **kwargs)
        Text(text, parent=self)


class Time(InlineElement):
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
        Text(datetime, parent=self)
