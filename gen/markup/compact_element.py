from textwrap import indent
from typing import Optional

from markup import Text
from markup.element import Element
from markup.node import Node
from markup.wrap import wrap_tokens


class CompactElement(Element):
    def __init__(self, name: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name=name, parent=parent, **kwargs)

    def markup(self, width: int) -> str:
        start = self.start_tag()
        end = self.end_tag()
        remaining_width = width - len(start) - len(end)

        tokens = []
        for child in self.children:
            tokens += child.tokens()

        content = ''.join(tokens)
        if content and len(content) > remaining_width:
            prefix = '    '
            child_width = width - len(prefix)
            wrapped_tokens = wrap_tokens(tokens, child_width)
            if wrapped_tokens[-1].isspace():
                wrapped_tokens[-1] = '\n'
            else:
                wrapped_tokens.append('\n')
            wrapped_content = ''.join(wrapped_tokens)
            if self.omit_end_tag():
                return start + '\n' + indent(wrapped_content, prefix)
            else:
                return start + '\n' + indent(wrapped_content, prefix) + end + '\n'
        else:
            if self.omit_end_tag():
                return start + content + '\n'
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


class FigCaption(CompactElement):
    def __init__(self, text: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='figcaption', parent=parent, **kwargs)
        Text(text, parent=self)


class H1(CompactElement):
    def __init__(self, text: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='h1', parent=parent, **kwargs)
        Text(text, parent=self)


class H2(CompactElement):
    def __init__(self, text: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='h2', parent=parent, **kwargs)
        Text(text, parent=self)


class Label(CompactElement):
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


class Li(CompactElement):
    def __init__(
            self,
            text: Optional[str] = None,
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
        if text:
            Text(text, parent=self)

    def omit_end_tag(self) -> bool:
        if self.next_sibling:
            return isinstance(self.next_sibling, Li)
        else:
            return True


class Script(CompactElement):
    def __init__(
            self,
            src: str,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(name='script', parent=parent, **kwargs)
        self.attributes['src'] = src


class Title(CompactElement):
    def __init__(self, title: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='title', parent=parent, **kwargs)
        Text(title, parent=self)
