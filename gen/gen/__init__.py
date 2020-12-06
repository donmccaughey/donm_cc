from __future__ import annotations

import os
from typing import Optional


with_parent: list[Optional[Parent]] = [None]


class WithParent:
    pass


class Child:
    def __init__(
            self,
            name: str,
            parent: Optional[Parent]=None,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.name = name
        self.parent = parent if parent else with_parent[-1]
        if self.parent:
            self.parent.children.append(self)

    @property
    def dirname(self) -> str:
        return self.parent.dirname

    @property
    def filename(self) -> Optional[str]:
        return self.name

    @property
    def path(self) -> str:
        return self.dirname + (self.filename if self.filename else '')

    @property
    def rank(self) -> int:
        return self.parent.rank + 1 if self.parent else 0


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
        global with_parent
        with_parent.append(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        with_parent.pop()

    @property
    def all(self) -> list:
        all = [self]
        for child in self.children:
            if hasattr(child, 'all'):
                all += child.all
            else:
                all.append(child)
        return all

    @property
    def dirname(self) -> str:
        return self.parent.dirname if self.parent else './'

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
