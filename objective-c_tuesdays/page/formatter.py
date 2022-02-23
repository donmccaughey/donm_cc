from bs4.element import Doctype, NavigableString, Tag, PageElement
from page import Page


class Formatter:
    def __init__(self):
        self.line = 1
        self.offset = 0
        self.out = ''

    def format(self, page: Page) -> str:
        self.node(page.document)
        return self.out

    def write(self, s: str):
        for ch in s:
            if ch == '\n':
                self.line += 1
                self.offset = 0
            else:
                self.offset += 1
        self.out += s

    def ensure_newline(self):
        if self.out and not self.out[-1].endswith('\n'):
            self.write('\n')

    def node(self, node: PageElement):
        match node:
            case Doctype():
                self.doctype(node)
            case NavigableString():
                self.text(node)
            case Tag():
                self.element(node)
            case _:
                raise RuntimeError(f'Unexpected PageElement: {node}')

    def doctype(self, doctype: Doctype):
        self.write(f'<!doctype {doctype}>\n')

    def document(self, document: Tag):
        for child in document.children:
            self.node(child)

    def text(self, text: NavigableString):
        self.write(str(text))

    def element(self, element: Tag):
        if is_document(element):
            self.document(element)
        elif is_block(element):
            self.block_element(element)
        elif is_omittable(element):
            self.omittable_element(element)
        else:
            self.inline_element(element)

    def block_element(self, element: Tag):
        self.ensure_newline()
        self.write(start_tag(element))
        self.ensure_newline()
        for child in element.children:
            self.node(child)
        self.ensure_newline()
        if has_end_tag(element):
            self.write(end_tag(element))
            self.ensure_newline()

    def inline_element(self, element: Tag):
        self.write(start_tag(element))
        for child in element.children:
            self.node(child)
        if has_end_tag(element):
            self.write(end_tag(element))

    def omittable_element(self, element: Tag):
        for child in element.children:
            self.node(child)


def is_block(element: Tag) -> bool:
    return element.name in [
        'div', 'meta', 'ol', 'p', 'pre', 'table', 'ul'
    ]


def is_document(element: Tag) -> bool:
    return element.name == '[document]'


def is_omittable(element: Tag) -> bool:
    return len(element.attrs) == 0 and element.name in ['body', 'head', 'html']


def has_end_tag(element: Tag) -> bool:
    return element.name not in ['meta']


def q(value: str) -> str:
    return f"'{value}'"


def start_tag(element: Tag) -> str:
    parts = [f'<{element.name}']
    if len(element.attrs):
        for name in sorted(element.attrs.keys()):
            value = element.attrs[name]
            if isinstance(value, list):
                value = ' '.join(value)
            parts.append(f" {name}={q(value)}")
    parts.append('>')
    return ''.join(parts)


def end_tag(element: Tag):
    return f'</{element.name}>'
