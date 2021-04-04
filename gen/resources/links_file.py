from typing import Optional

from file_formats.links_page.parser import parse
from markup import Section, H1, P, Ul
from website.links import link as build_link
from .directory import Directory
from .page import Page


class LinksFile(Page):
    def __init__(
            self,
            source: str,
            parent: Optional[Directory] = None,
            **kwargs,
    ):
        with open(source) as f:
            contents = f.read()
            links_page = parse(contents)

        super().__init__(
            title=links_page.title,
            parent=parent,
            **kwargs,
        )

        self.source = source
        self.links_page = links_page
        with self.body_content:
            with Section(class_names=['overview']):
                H1(links_page.title)
                for note in links_page.notes:
                    P(note)
            for section in links_page.sections:
                with Section(class_names=['links']):
                    H1(section.title)
                    for note in section.notes:
                        P(note)
                    with Ul():
                        for link in section.links:
                            build_link(
                                type=link.type,
                                title=link.title,
                                href=link.link,
                                authors=link.authors,
                                date=link.date,
                                checked=link.checked,
                            )
