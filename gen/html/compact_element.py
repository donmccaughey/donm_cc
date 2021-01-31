from textwrap import indent
from typing import Optional

from html import Format, Text
from html.element import Element
from html.node import Node
from html.wrap import wrap_tokens


class CompactElement(Element):
    def __init__(self, name: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name=name, parent=parent, **kwargs)
        self.format = Format.COMPACT

    def markup(self, width: int) -> str:
        start = self.start_tag()
        end = self.end_tag()
        remaining_width = width - len(start) - len(end)

        tokens = []
        for child in self.children:
            tokens += child.tokens()

        content = ''.join(tokens)
        if len(content) > remaining_width:
            prefix = '    '
            child_width = width - len(prefix)
            wrapped = wrap_tokens(tokens, child_width)
            if wrapped[-1].isspace():
                wrapped[-1] = '\n'
            else:
                wrapped.append('\n')
            s = ''.join(wrapped)
            return start + '\n' + indent(s, prefix) + end + '\n'
        else:
            return start + content + end + '\n'


class Button(CompactElement):
    def __init__(
            self,
            text: str,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(name='button', parent=parent, **kwargs)
        Text(text, parent=self)


class CompactA(CompactElement):
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


class CompactSpan(CompactElement):
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


class CompactTime(CompactElement):
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


class H1(CompactElement):
    def __init__(self, text: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='h1', parent=parent, **kwargs)
        Text(text, parent=self)


class H2(CompactElement):
    def __init__(self, text: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='h2', parent=parent, **kwargs)
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
        if for_id:
            self.attributes['for'] = for_id
        Text(text, parent=self)


class Title(CompactElement):
    def __init__(self, title: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='title', parent=parent, **kwargs)
        Text(title, parent=self)
