from __future__ import annotations
import os
from typing import Optional, Tuple
from markup import *
from markup.node import with_node
from .directory import Directory
from .resource import Resource


def make_name(title: str):
    lowered = title.lower()
    return lowered.replace(' ', '_')


class Page(Resource):
    def __init__(
            self,
            title: str,
            parent: Optional[Directory] = None,
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
        self.document = None

    def __enter__(self):
        with_node.append(self.body_content)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with_node.pop()

    def find_nav_links(self) -> list[Tuple[str, str]]:
        directories = self.find_directories()
        if not directories:
            return [(self.url, self.title)]

        nav_links = []
        for directory in directories:
            index = directory.find_index_page()
            if not index:
                continue
            if directory.is_root or index is not self:
                nav_links.append((directory.url, index.title))
        return nav_links

    def file_parts(self) -> list[str]:
        return [self.name + '.html']

    def add_script(self, src: str):
        with self.head_content:
            Script(src=src)

    def add_stylesheet(self, src: str):
        with self.head_content:
            Stylesheet(src)

    def build_documents(self):
        self.document = Document()
        with self.document:
            DocType()
            with HTML(lang='en'):
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
            if omit_styles:
                self.document.detach_descendants(lambda node: isinstance(node, Stylesheet))

            mode = 'w' if overwrite else 'x'
            with open(path, mode, encoding='utf8') as f:
                f.write(self.document.markup(80))

    def accumulate_links(self, links: list[(Resource, str)]):
        nodes = []
        self.document.accumulate_nodes(nodes)
        for node in nodes:
            if isinstance(node, A):
                a: A = node
                href = a.attributes['href']
                if href:
                    links.append((self, href))
