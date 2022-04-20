from typing import Optional

import os

from file_formats.page_file import Link, BookLink
from file_formats.page_file.parser import parse
from markdown import inline_markdown_to_markup
from markup import Section, H1, P, Ul
from .directory import Directory
from .page import Page


class PageFile(Page):
    EXT = '.page'

    def __init__(
            self,
            source: str,
            parent: Optional[Directory] = None,
            **kwargs,
    ):
        with open(source) as f:
            contents = f.read()
            page_file = parse(contents)

        basename = os.path.basename(source)
        name = basename.split('.')[0]

        super().__init__(
            title=page_file.title,
            name=name,
            parent=parent,
            **kwargs,
        )

        self.source = source
        self.page_file = page_file
        with self.body_content:
            with Section(class_names=['overview']):
                H1(page_file.full_title)
                for note in page_file.notes:
                    with P():
                        inline_markdown_to_markup(note)
            for section in page_file.sections:
                with Section(class_names=['links']):
                    H1(section.title)
                    for note in section.notes:
                        with P():
                            inline_markdown_to_markup(note)
                    with Ul():
                        for link in section.links:
                            self.link(link)

    def link(self, link: BookLink | Link):
        from website.links import book, link as general_link

        match link:
            case BookLink():
                book(
                    title=link.title,
                    href=link.url,
                    asin=link.asin,
                    authors=link.authors,
                    date=link.date,
                    checked=link.checked,
                )
            case Link():
                general_link(
                    modifier=link.modifier,
                    title=link.title,
                    href=link.url,
                    authors=link.authors,
                    date=link.date,
                    checked=link.checked,
                )
