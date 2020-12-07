from __future__ import annotations

import os
from typing import Optional


_with_parent: list[Optional[Parent]] = [None]


class Child:
    def __init__(
            self,
            name: str,
            parent: Optional[Parent]=None,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.name = name
        self.parent = parent if parent else _with_parent[-1]
        if self.parent:
            self.parent.children.append(self)

    def __lt__(self, other: Child) -> bool:
        return self.path_parts < other.path_parts

    @property
    def dirname(self) -> str:
        return ('/'.join(self.dir_parts) + '/') if self.dir_parts else './'

    @property
    def dir_parts(self) -> list[str]:
        return self.parent.dir_parts if self.parent else []

    @property
    def filename(self) -> Optional[str]:
        return self.file_parts[0] if self.file_parts else None

    @property
    def file_parts(self) -> list[str]:
        return [self.name]

    @property
    def path(self) -> str:
        return ('./' + '/'.join(self.path_parts)) if self.path_parts else './'

    @property
    def path_parts(self) -> list[str]:
        return self.dir_parts + self.file_parts

    @property
    def rank(self) -> int:
        return self.parent.rank + 1 if self.parent else 0

    @property
    def url(self) -> str:
        return ('/' + '/'.join(self.path_parts)) if self.path_parts else '/'

    def generate(self, output_path: str, is_dry_run=True):
        raise NotImplementedError


class Parent(Child):
    def __init__(
            self,
            has_files: bool,
            parent: Optional[Parent]=None,
            **kwargs,
    ):
        super().__init__(parent=parent, **kwargs)
        self.children: list[Child] = []
        self.has_files = has_files

    def __enter__(self):
        global _with_parent
        _with_parent.append(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        _with_parent.pop()

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
                            File(source, self)
        for child in self.children:
            if hasattr(child, 'find_files'):
                child.find_files(source_dir)

    def should_include_file(self, name: str) -> bool:
        return not name.startswith('.')


from .directory import Directory
from .file import File
from .index_page import IndexPage
from .page import Page
