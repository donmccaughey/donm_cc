from __future__ import annotations
import os
from typing import Optional

import resources
from . import with_parent
from .resource import Resource


class Directory(Resource):
    def __init__(
            self,
            name: str,
            parent: Optional[Directory] = None,
            is_root: bool = False,
            has_files: bool = True,
            **kwargs,
    ):
        super().__init__(
            name=name,
            parent=parent,
            **kwargs,
        )
        self.children: list[Resource] = []
        self.is_root = is_root
        self.has_files = has_files

    def __enter__(self):
        with_parent.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with_parent.pop()

    def dir_parts(self) -> list[str]:
        return (
                (self.parent.dir_parts() if self.parent else [])
                + ([] if self.is_root else [self.name])
        )

    def file_parts(self) -> list[str]:
        return []

    @property
    def path(self) -> str:
        return './' if self.is_root else './' + self.dirname

    @property
    def url(self) -> str:
        dir_parts = self.dir_parts()
        return ('/' + '/'.join(dir_parts) + '/') if dir_parts else '/'

    @property
    def all(self) -> list:
        all = [self]
        for child in sorted(self.children):
            if hasattr(child, 'all'):
                all += child.all
            else:
                all.append(child)
        return all

    def find_files(self, source_dir: str):
        path = os.path.join(os.getcwd(), source_dir)
        path = os.path.join(path, self.dirname)
        path = os.path.normpath(path)
        if self.has_files:
            with os.scandir(path) as dir:
                for entry in dir:
                    if entry.is_file():
                        if self.should_include_file(entry.name):
                            source = os.path.join(path, entry.name)
                            source = os.path.normpath(source)
                            source = os.path.relpath(source)
                            if source.endswith('.links.txt'):
                                resources.page_file.PageFile(source, self)
                            else:
                                resources.file.File(source, self)
        for child in self.children:
            if hasattr(child, 'find_files'):
                child.find_files(source_dir)

    def find_index_page(self) -> Optional[resources.page.Page]:
        for child in self.children:
            if isinstance(child, resources.page.Page) and child.name == 'index':
                return child
        return None

    def should_include_file(self, name: str) -> bool:
        return not name.startswith('.')

    def generate(
            self,
            output_path: str,
            is_dry_run=True,
            overwrite=False,
            omit_styles=False,
    ):
        path = os.path.join(output_path, self.path)
        path = os.path.normpath(path)
        print('creating directory', path)
        if not is_dry_run:
            os.makedirs(path, exist_ok=overwrite)
        for child in self.children:
            child.generate(output_path, is_dry_run, overwrite)
