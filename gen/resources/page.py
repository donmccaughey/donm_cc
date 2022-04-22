from __future__ import annotations

import os
from functools import reduce
from typing import Optional, Tuple

from css import parse_css_file
from markup import *
from markup.block_element import Style
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

    def find_links(self) -> list[Tuple[Resource, str]]:
        nodes = []
        self.document.accumulate_nodes(nodes)
        links = []
        for node in nodes:
            if isinstance(node, A):
                a: A = node
                href = a.attributes['href']
                if href:
                    # TODO: create absolute path for link
                    links.append((self, href))
        return links

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

    def merge_stylesheets(self, source_dir: str):
        assert self.document
        stylesheets = []
        for node in self.document:
            if isinstance(node, Stylesheet):
                stylesheets.append(node)

        css_files = []
        parent = None
        sibling = None
        for stylesheet in stylesheets:
            if not parent:
                parent = stylesheet.parent
            if not sibling:
                sibling = stylesheet.previous_sibling

            href = stylesheet.attributes['href']
            if os.path.isabs(href):
                path = os.path.join(source_dir, href[1:])
            else:
                path = os.path.join(source_dir, self.dirname, href)

            css_files.append(parse_css_file(path))
            stylesheet.detach()

        if css_files:
            css = reduce(lambda a, b: a + b, css_files)
            style = Style(str(css))
            if sibling:
                sibling.insert_after(style)
            else:
                style.attach(parent)

    def remove_stylesheets(self):
        assert self.document
        self.document.detach_descendants(
            lambda node: isinstance(node, Stylesheet)
        )

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
                                Text(' \u2022 ')
                            A(href=url, text=title)
                    body.attach_children(self.body_content.detach_children())

    def generate(
            self,
            output_dir: str,
            is_dry_run=True,
            overwrite=False,
    ):
        path = os.path.join(output_dir, self.path)
        path = os.path.normpath(path)
        print('writing page', path)
        if not is_dry_run:
            mode = 'w' if overwrite else 'x'
            with open(path, mode, encoding='utf8') as f:
                f.write(self.document.markup(80))
