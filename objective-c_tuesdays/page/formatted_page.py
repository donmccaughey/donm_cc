from typing import List

from bs4.element import Doctype, NavigableString, Tag, PageElement

from page import Page


class FormattedPage:
    def __init__(self, page: Page):
        self.indent = ''
        self.line = 1
        self.max_width = 80
        self.offset = 0
        self.out = ''
        self.page = page
        self.wrap = False
        self.wrap_buffer = []

    def __str__(self) -> str:
        self.__node(self.page.document)
        self.__write('\n')
        return self.out

    def __write(self, s: str, wrappable: bool=False):
        if self.wrap:
            if wrappable:
                self.wrap_buffer.extend(divide_words(s))
            else:
                self.wrap_buffer.append(s)
        else:
            self.__chars_out(s)

    def __chars_out(self, s: str):
        for ch in s:
            if ch == '\n':
                self.line += 1
                self.offset = 0
                self.out += ch
                self.offset += len(self.indent)
                self.out += self.indent
            else:
                self.offset += 1
                self.out += ch

    def __is_at_line_start(self) -> bool:
        return self.offset == len(self.indent)

    def __is_too_long(self, word: str) -> bool:
        return self.offset + len(word) > self.max_width

    def __wrap_on(self):
        self.wrap = True

    def __wrap_off(self):
        self.wrap = False
        wrap_buffer = join_unwrappable_words(self.wrap_buffer)
        for word in wrap_buffer:
            # TODO: trim leading/trailing spaces
            # TODO: two spaces after a period
            if self.__is_too_long(word) and not self.__is_at_line_start():
                self.__chars_out('\n')
            self.__chars_out(word)
        self.wrap_buffer = []

    def __indent(self):
        self.indent += '    '

    def __unindent(self):
        self.indent = self.indent[0:-4]

    def __ensure_newline(self):
        if self.out and not self.out.endswith('\n' + self.indent):
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
        self.__write(html_encode(str(text)), wrappable=True)

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
        self.__indent()
        self.__ensure_newline()
        if should_wrap_content(element):
            self.__wrap_on()
        for child in element.children:
            self.__node(child)
        if should_wrap_content(element):
            self.__wrap_off()
        self.__unindent()
        if has_end_tag(element):
            self.__ensure_newline()
            self.__write(end_tag(element))

    def __compact(self, element: Tag):
        self.__ensure_newline()
        self.__write(start_tag(element))
        if element.name == 'pre':
            old_indent = self.indent
            self.indent = ''
        for child in element.children:
            self.__node(child)
        if element.name == 'pre':
            self.indent = old_indent
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
        'aside', 'br', 'div', 'footer', 'li', 'nav', 'ol', 'p',
        'section', 'table', 'tr', 'ul'
    ]


def is_compact(element: Tag) -> bool:
    return element.name in ['h1', 'h2', 'link', 'meta', 'pre', 'title']


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


def should_wrap_content(element: Tag) -> bool:
    return element.name in ['footer', 'li', 'p']


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


def divide_words(s: str) -> List[str]:
    words = []
    begin = 0
    end = 0
    while end < len(s):
        if s[end].isspace():
            end += 1
            words.append(s[begin:end])
            begin = end
        else:
            end += 1
    if begin < end:
        words.append(s[begin:end])
    return words


def join_unwrappable_words(words: List[str]) -> List[str]:
    first_word = words[0]
    new_words = [first_word]
    last_word = first_word
    for word in words[1:]:
        if not last_word[-1].isspace() and not word[0].isspace():
            new_words.pop()
            word = last_word + word
        new_words.append(word)
        last_word = word
    return new_words
