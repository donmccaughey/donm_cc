import os
from typing import Optional

from site import Child, Parent
from tags import DocType, Document, HTML, Head, Meta, Title, Link, Body, H1


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

    @property
    def document(self) -> Document:
        document = Document()
        with document:
            DocType()
            with HTML(lang='en'):
                with Head():
                    Meta({'charset': 'utf-8'})
                    Meta({
                        'name': 'viewport',
                        'content': 'initial-scale=0.9, width=device-width',
                    })
                    Title(self.title)
                    Link({
                        'rel': 'stylesheet',
                        'href': '/base.css',
                    })
                with Body():
                    H1(self.title)
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
