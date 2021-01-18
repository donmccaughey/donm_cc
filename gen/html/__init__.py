from textwrap import TextWrapper, dedent
from .doctype import DocType
from .document import Document
from .format import Format
from .tag import Tag
from .tag_type import TagType
from .text import Text
from .elements import A, Body, Button, Code, Div, Em, Form, H1, H2, Head, HTML
from .elements import Label, Li, Nav, P, Script, Section, Span, Strong, Time
from .elements import Title, Ul
from .empty_element import Br, Img, Input, Link, Meta, MetaCharset
from .empty_element import MetaCharset, MetaViewport, Stylesheet


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

        if tag.type == TagType.COMMENT:
            parts += ['\n', indent(level), tag.text]
        elif tag.type == TagType.DTD:
            parts += [tag.text]
        elif tag.type == TagType.START:
            if tag.format == Format.INLINE:
                parts += ['\n', indent(level), tag.text]
            else:
                parts += ['\n', indent(level), tag.text]
                level += (1 if tag.indent_children else 0)
        elif tag.type == TagType.END:
            if tag.format == Format.INLINE:
                if not tag.omit:
                    parts += [tag.text]
            elif tag.format == Format.COMPACT:
                level -= (1 if tag.indent_children else 0)
                parts += [tag.text]
            else:
                level -= (1 if tag.indent_children else 0)
                if not tag.omit:
                    parts += ['\n', indent(level), tag.text]
        elif tag.type == TagType.TEXT:
            text = clean_text(tag.text)
            if (
                    previous_tag.type == TagType.START
                    and not previous_tag.format == Format.BLOCK
            ):
                parts += [text]
            else:
                parts += ['\n', wrap_text(text, level)]
        else:
            raise RuntimeError

    return ''.join(parts) + '\n'
