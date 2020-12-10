import os
from typing import Optional

from site import Child, Parent
from tags import *
from tags.node import with_node


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
        self.page_content = Document()

    def __enter__(self):
        with_node.append(self.page_content)

    def __exit__(self, exc_type, exc_val, exc_tb):
        with_node.pop()

    @property
    def document(self) -> Document:
        document = Document()
        with document:
            DocType()
            with HTML(lang='en'):
                with Head():
                    MetaCharset('utf-8')
                    MetaViewport(initial_scale='0.9', width='device-width')
                    Title(self.title)
                    Stylesheet(href='/base.css')
                content_root = Body()
                with content_root:
                    with Nav(class_names=['menu']):
                        ancestors = self.ancestors
                        if ancestors:
                            for ancestor in self.ancestors:
                                if hasattr(ancestor, 'title'):
                                    A(href=ancestor.url, text=ancestor.title)
                        else:
                            A(href=self.url, text=self.title)
                    for child in self.page_content.children:
                        child.detach()
                        content_root.children.append(child)
        return document

    @property
    def file_parts(self) -> list[str]:
        return [self.name + '.html']

    def generate(self, output_path: str, is_dry_run: bool = True):
        path = os.path.join(output_path, self.path)
        path = os.path.normpath(path)
        print('writing page', path)
        if not is_dry_run:
            with open(path, 'x', encoding='utf8') as f:
                f.write(str(self.document))
