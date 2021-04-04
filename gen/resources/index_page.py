from __future__ import annotations
import os
from typing import Optional

from .page import Page
from .parent import Parent


class IndexPage(Parent, Page):
    def __init__(
            self,
            title: str,
            parent: Optional[Parent] = None,
            name: Optional[str] = None,
            is_root: bool = False,
            has_files: bool = False,
            **kwargs,
    ):
        super().__init__(
            has_files=has_files,
            name=name,
            parent=parent,
            title=title,
            **kwargs,
        )
        self.is_root = is_root

    def __enter__(self):
        Parent.__enter__(self)
        Page.__enter__(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Parent.__exit__(self, exc_type, exc_val, exc_tb)
        Page.__exit__(self, exc_type, exc_val, exc_tb)

    @property
    def dir_parts(self) -> list[str]:
        return (
                (self.parent.dir_parts if self.parent else [])
                + ([] if self.is_root else [self.name])
        )

    @property
    def file_parts(self) -> list[str]:
        return ['index.html']

    def generate(
            self,
            output_path: str,
            is_dry_run=True,
            overwrite=False,
            omit_styles=False,
    ):
        dirname = os.path.join(output_path, self.dirname)
        dirname = os.path.normpath(dirname)
        print('creating directory', dirname)
        if not is_dry_run:
            os.makedirs(dirname, exist_ok=overwrite)
        path = os.path.join(output_path, self.path)
        path = os.path.normpath(path)
        print('writing index page', path)
        self.write_page(path, is_dry_run, overwrite, omit_styles)
        for child in self.children:
            child.generate(output_path, is_dry_run, overwrite, omit_styles)

    def should_include_file(self, name: str) -> bool:
        if name in ['index.html']:
            return False
        else:
            return super().should_include_file(name)
