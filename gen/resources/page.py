from __future__ import annotations
import os
from typing import Optional, TYPE_CHECKING
from .child import Child
from html import *
from html.node import with_node

if TYPE_CHECKING:
    from .parent import Parent


def make_name(title: str):
    lowered = title.lower()
    return lowered.replace(' ', '_')


class Page(Child):
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
        self.page_content = Document()

    def __enter__(self):
        with_node.append(self.page_content)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with_node.pop()

    @property
    def document(self) -> Document:
        document = Document()
        with document:
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
                        ancestors = self.ancestors
                        if ancestors:
                            for ancestor in self.ancestors:
                                if hasattr(ancestor, 'title'):
                                    A(href=ancestor.url, text=ancestor.title)
                        else:
                            A(href=self.url, text=self.title)
                    body.attach_children(self.page_content.detach_children())
        return document

    @property
    def file_parts(self) -> list[str]:
        return [self.name + '.html']

    def add_script(self, src: str, charset: Optional[str] = None):
        with self.head_content:
            Script(src=src, charset=charset)

    def add_stylesheet(self, src: str):
        with self.head_content:
            Stylesheet(src)

    def generate(
            self,
            output_path: str,
            is_dry_run: bool = True,
            overwrite = False,
    ):
        path = os.path.join(output_path, self.path)
        path = os.path.normpath(path)
        print('writing page', path)
        if not is_dry_run:
            mode = 'w' if overwrite else 'x'
            with open(path, mode, encoding='utf8') as f:
                f.write(str(self.document))
