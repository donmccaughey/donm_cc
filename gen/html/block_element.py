from textwrap import indent
from typing import Optional

from html import Text
from html.comment import Comment
from html.element import Element
from html.inline_element import InlineElement
from html.node import Node
from html.wrap import wrap_tokens


class BlockElement(Element):
    def __init__(self, name: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name=name, parent=parent, **kwargs)

    def markup(self, width: int) -> str:
        markup = ''
        if self.omit_start_tag() and self.omit_end_tag():
            self.indent_children = False
        else:
            markup += self.start_tag()
            markup += '\n'

        if self.children:
            prefix = '    ' if self.indent_children else ''
            child_width = width - len(prefix)
            tokens = []

            def append_tokens():
                nonlocal markup, tokens
                if tokens:
                    if tokens[0].isspace():
                        del tokens[0]
                    if tokens and tokens[-1].isspace():
                        del tokens[-1]
                    wrapped = wrap_tokens(tokens, child_width)
                    wrapped.append('\n')
                    s = ''.join(wrapped)
                    markup += indent(s, prefix)
                    tokens = []

            for child in self.children:
                if isinstance(child, InlineElement) or isinstance(child, Text):
                    tokens += child.tokens()
                else:
                    append_tokens()
                    markup += indent(child.markup(child_width), prefix)
            append_tokens()

        if not self.omit_end_tag():
            markup += self.end_tag()
            markup += '\n'
        return markup


class BlockA(BlockElement):
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


class Body(BlockElement):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='body', parent=parent, **kwargs)

    def omit_end_tag(self) -> bool:
        if self.next_sibling:
            return not isinstance(self.next_sibling, Comment)
        else:
            return True

    def omit_start_tag(self) -> bool:
        if not self.children:
            return True
        if isinstance(self.children[0], Comment):
            return False
        if isinstance(self.children[0], Element):
            return self.children[0].name not in [
                'meta', 'link', 'script', 'style', 'template'
            ]
        return True


class Div(BlockElement):
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


class Form(BlockElement):
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


class Head(BlockElement):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='head', parent=parent, **kwargs)

    def omit_end_tag(self) -> bool:
        if self.next_sibling:
            # A head element’s end tag may be omitted if the head element is
            # not immediately followed by a space character or a comment.
            return not isinstance(self.next_sibling, Comment)
        else:
            return True

    def omit_start_tag(self) -> bool:
        if self.children:
            return isinstance(self.children[0], Element)
        else:
            return True


class HTML(BlockElement):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='html', parent=parent, **kwargs)
        self.indent_children = False

    def omit_end_tag(self) -> bool:
        if self.next_sibling:
            return not isinstance(self.next_sibling, Comment)
        else:
            return True


class Nav(BlockElement):
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


class P(BlockElement):
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


class Section(BlockElement):
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


class Ul(BlockElement):
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
