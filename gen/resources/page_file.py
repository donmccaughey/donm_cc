from typing import Optional

import os
from file_formats.page_file.parser import parse
from markup import Section, H1, P, Ul
from website.links import link as build_link
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
                H1(page_file.title)
                for note in page_file.notes:
                    P(note)
            for section in page_file.sections:
                with Section(class_names=['links']):
                    H1(section.title)
                    for note in section.notes:
                        P(note)
                    with Ul():
                        for link in section.links:
                            build_link(
                                modifier=link.modifier,
                                title=link.title,
                                href=link.link,
                                authors=link.authors,
                                date=link.date,
                                checked=link.checked,
                            )
