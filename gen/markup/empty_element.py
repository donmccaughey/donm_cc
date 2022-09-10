from typing import Optional, List

from markup.element import Element
from markup.node import Node


class EmptyElement(Element):
    def __init__(self, name: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(name=name, parent=parent, **kwargs)

    def markup(self, width: int) -> str:
        return self.start_tag() + '\n'

    def omit_end_tag(self) -> bool:
        return True

    def tokens(self) -> List[str]:
        return [self.start_tag() + '\n']


class Br(EmptyElement):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='br', parent=parent, **kwargs)


class Img(EmptyElement):
    def __init__(
            self,
            src: str,
            alt: str,
            parent: Optional[Node] = None,
            **kwargs,
    ):
        super().__init__(name='img', parent=parent, **kwargs)
        self.attributes['src'] = src
        self.attributes['alt'] = alt


class Input(EmptyElement):
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
        super().__init__(name='input', parent=parent, **kwargs)
        self.attributes['id'] = id
        self.attributes['name'] = name if name else id
        if type:
            self.attributes['type'] = type
        if value:
            self.attributes['value'] = value
        if checked:
            self.attributes['checked'] = None


class Link(EmptyElement):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='link', parent=parent, **kwargs)


class IconLink(Link):
    def __init__(self, href: str, parent: Optional[Node] = None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.attributes['rel'] = 'icon'
        self.attributes['href'] = href


class Meta(EmptyElement):
    def __init__(self, parent: Optional[Node] = None, **kwargs):
        super().__init__(name='meta', parent=parent, **kwargs)


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


class Stylesheet(Link):
    def __init__(self, href: str, for_js: bool = False, parent: Optional[Node] = None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.attributes['rel'] = 'stylesheet'
        self.attributes['href'] = href
        self.for_js = for_js
