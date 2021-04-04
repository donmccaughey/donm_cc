from __future__ import annotations
import os
from typing import Optional, TYPE_CHECKING, Tuple

from .resource import Resource
from .directory import Directory
from markup import *
from markup.node import with_node

if TYPE_CHECKING:
    from .parent import Parent


def make_name(title: str):
    lowered = title.lower()
    return lowered.replace(' ', '_')


class Page(Resource):
    def __init__(
            self,
            title: str,
            parent: Optional[Parent] = None,
            name: Optional[str] = None,
            **kwargs
    ):
        super().__init__(
            name=name if name is not None else make_name(title),
            parent=parent,
            **kwargs,
        )
        self.title = title
        self.head_content = Document()
        self.body_content = Document()

    def __enter__(self):
        with_node.append(self.body_content)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with_node.pop()

    def build_document(self) -> Document:
        document = Document()
        with document:
            DocType()
            with HTML():
                with Head() as head:
                    MetaCharset('utf-8')
                    MetaViewport(initial_scale='0.9', width='device-width')
                    Title(self.title)
                    Stylesheet(href='/base.css')
                    head.attach_children(self.head_content.detach_children())
                with Body() as body:
                    with Nav(class_names=['menu']):
                        nav_links = self.find_nav_links()
                        for i, (url, title) in enumerate(nav_links):
                            if i:
                                Text(' &bull; ')
                            A(href=url, text=title)
                    body.attach_children(self.body_content.detach_children())
        return document

    def find_nav_links(self) -> list[Tuple[str, str]]:
        ancestors = self.find_ancestors()
        if not ancestors:
            return [(self.url, self.title)]

        nav_links = []
        for ancestor in ancestors:
            if isinstance(ancestor, Page):
                nav_links.append((ancestor.url, ancestor.title))
            elif isinstance(ancestor, Directory):
                index = ancestor.find_index_page()
                if not index:
                    continue
                if ancestor.is_root or index is not self:
                    nav_links.append((ancestor.url, index.title))
        return nav_links

    def file_parts(self) -> list[str]:
        return [self.name + '.html']

    def add_script(self, src: str):
        with self.head_content:
            Script(src=src)

    def add_stylesheet(self, src: str):
        with self.head_content:
            Stylesheet(src)

    def generate(
            self,
            output_path: str,
            is_dry_run=True,
            overwrite=False,
            omit_styles=False,
    ):
        path = os.path.join(output_path, self.path)
        path = os.path.normpath(path)
        print('writing page', path)
        self.write_page(path, is_dry_run, overwrite, omit_styles)

    def write_page(
            self,
            path: str,
            is_dry_run: bool,
            overwrite: bool,
            omit_styles: bool,
    ):
        if not is_dry_run:
            document = self.build_document()
            if omit_styles:
                detached = document.detach_descendants(lambda node: isinstance(node, Stylesheet))

            mode = 'w' if overwrite else 'x'
            with open(path, mode, encoding='utf8') as f:
                f.write(document.markup(80))
