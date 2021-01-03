from textwrap import TextWrapper, dedent
from .doctype import DocType
from .document import Document
from .format import Format
from .tag import Tag, TagType
from .text import Text
from .elements import A, Body, Br, Button, Code, Div, Em, Form, H1, H2, Head, HTML
from .elements import Img, Input, Label, Li, MetaCharset, MetaViewport, Nav, P
from .elements import Script, Section, Span, Strong, Stylesheet, Time, Title, Ul


def indent(level: int) -> str:
    return '    ' * level


def trim_blank_lines(lines: list[str]) -> list[str]:
    return [line for line in lines if line.strip()]


def clean_text(text: str) -> str:
    lines = text.splitlines()
    trimmed_lines = trim_blank_lines(lines)
    trimmed_text = '\n'.join(trimmed_lines)
    return dedent(trimmed_text)


def wrap_text(text: str, level: int) -> str:
    wrapper = TextWrapper(
        width=80,
        initial_indent=indent(level),
        subsequent_indent=indent(level),
        fix_sentence_endings=True,
    )
    return wrapper.fill(text)


def format_tags(tags: list[Tag]) -> str:
    parts = []
    level = 0

    for i, tag in enumerate(tags):
        previous_tag = tags[i - 1]

        if tag.is_dtd:
            parts += [tag.text]
        elif tag.is_start:
            if tag.is_inline:
                if previous_tag.is_inline:
                    parts += ['\n', indent(level), tag.text]
                else:
                    parts += ['\n', indent(level), tag.text]
            elif tag.is_compact:
                parts += ['\n', indent(level), tag.text]
                level += (1 if tag.indent_children else 0)
            else:
                parts += ['\n', indent(level), tag.text]
                level += (1 if tag.indent_children else 0)
        elif tag.is_end:
            if tag.is_inline:
                if tag.has_end_tag:
                    parts += [tag.text]
            elif tag.is_compact:
                level -= (1 if tag.indent_children else 0)
                parts += [tag.text]
            else:
                level -= (1 if tag.indent_children else 0)
                if tag.has_end_tag:
                    parts += ['\n', indent(level), tag.text]
        elif tag.is_text:
            text = clean_text(tag.text)
            if previous_tag.is_start and not previous_tag.is_block:
                parts += [text]
            else:
                parts += ['\n', wrap_text(text, level)]
        else:
            raise RuntimeError

    return ''.join(parts) + '\n'
