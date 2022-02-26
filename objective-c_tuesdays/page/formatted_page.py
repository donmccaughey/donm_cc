from bs4.element import Doctype, NavigableString, Tag, PageElement

from page import Page


class FormattedPage:
    def __init__(self, page: Page):
        self.indent_stack = [0]
        self.line = 1
        self.offset = 0
        self.out = ''
        self.page = page

    def __str__(self) -> str:
        self.__node(self.page.document)
        return self.out

    def __write(self, s: str):
        for ch in s:
            if ch == '\n':
                self.line += 1
                self.offset = 0
                self.out += ch
                if self.indent_stack[-1]:
                    indent = self.__get_indent()
                    self.offset += len(indent)
                    self.out += indent
            else:
                self.offset += 1
                self.out += ch

    def __get_indent(self):
        return ' ' * (4 * self.indent_stack[-1])

    def __indent(self):
        current = self.indent_stack[-1]
        self.indent_stack.append(current + 1)

    def __no_indent(self):
        self.indent_stack.append(0)

    def __unindent(self):
        self.indent_stack.pop()

    def __ensure_newline(self):
        if self.out and not self.out[-1].endswith('\n'):
            self.__write('\n')

    def __node(self, node: PageElement):
        match node:
            case Doctype():
                self.__doctype(node)
            case NavigableString():
                self.__text(node)
            case Tag():
                self.__element(node)
            case _:
                raise RuntimeError(f'Unexpected PageElement: {node}')

    def __doctype(self, doctype: Doctype):
        self.__write(f'<!doctype {doctype}>\n')

    def __document(self, document: Tag):
        for child in document.children:
            self.__node(child)

    def __text(self, text: NavigableString):
        self.__write(html_encode(str(text)))

    def __element(self, element: Tag):
        if is_document(element):
            self.__document(element)
        elif is_block(element):
            self.__block(element)
        elif is_compact(element):
            self.__compact(element)
        elif is_omittable(element):
            self.__omittable(element)
        else:
            self.__inline(element)

    def __block(self, element: Tag):
        self.__ensure_newline()
        self.__write(start_tag(element))
        # self.__no_indent() if element.name == 'pre' else self.__indent()
        self.__ensure_newline()
        for child in element.children:
            self.__node(child)
        # self.__unindent()
        self.__ensure_newline()
        if has_end_tag(element):
            self.__write(end_tag(element))
            self.__ensure_newline()

    def __compact(self, element: Tag):
        self.__ensure_newline()
        self.__write(start_tag(element))
        for child in element.children:
            self.__node(child)
        if has_end_tag(element):
            self.__write(end_tag(element))
            self.__ensure_newline()

    def __inline(self, element: Tag):
        self.__write(start_tag(element))
        for child in element.children:
            self.__node(child)
        if has_end_tag(element):
            self.__write(end_tag(element))

    def __omittable(self, element: Tag):
        for child in element.children:
            self.__node(child)


def html_encode(text: str) -> str:
    encoded = text.replace('&', '&amp;')
    encoded = encoded.replace('<', '&lt;')
    return encoded


def is_block(element: Tag) -> bool:
    return element.name in [
        'aside', 'br', 'div', 'footer', 'li', 'link', 'meta', 'nav', 'ol', 'p',
        'section', 'table', 'tr', 'ul'
    ]


def is_compact(element: Tag) -> bool:
    return element.name in ['h1', 'h2', 'pre', 'title']


def is_document(element: Tag) -> bool:
    return element.name == '[document]'


def is_omittable(element: Tag) -> bool:
    return (
            len(element.attrs) == 0
            and element.name in ['body', 'head', 'html', 'tbody']
    )


def has_end_tag(element: Tag) -> bool:
    return element.name not in [
        'br', 'hr', 'html', 'img', 'li', 'link', 'meta', 'p'
    ]


def should_indent_children(element: Tag) -> bool:
    return element.name not in ['body', 'head', 'html', 'pre']


# See "ASCII whitespace" in https://infra.spec.whatwg.org/#ascii-whitespace
ASCII_WHITESPACE = {
    '\t',  # tab
    '\n',  # new line
    '\f',  # form feed
    '\r',  # carriage return
    ' ',
}

# See "Unquoted attribute value syntax" in section 13.1.2.3 "Attributes" of
# https://html.spec.whatwg.org/multipage/syntax.html#attributes-2
SPECIAL_CHARS = ASCII_WHITESPACE | {
    '"',
    "'",
    '=',
    '<',
    '>',
    '`',
}


def q(attribute_value: str) -> str:
    if attribute_value == '':
        return "''"

    attribute_value_chars = set(attribute_value)

    if "'" in attribute_value_chars:
        if '"' in attribute_value_chars:
            attribute_value = attribute_value.replace('"', '&quot;')
        return f'"{attribute_value}"'

    if attribute_value_chars & SPECIAL_CHARS:
        return f"'{attribute_value}'"

    return attribute_value


def start_tag(element: Tag) -> str:
    s = f'<{element.name}'
    if len(element.attrs):
        for name in sorted(element.attrs.keys()):
            value = element.attrs[name]
            if isinstance(value, list):
                value = ' '.join(value)
            s += f" {name}={q(value)}"
    if s.endswith('/'):
        s += ' '
    s += '>'
    return s


def end_tag(element: Tag):
    return f'</{element.name}>'
