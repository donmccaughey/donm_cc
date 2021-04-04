from __future__ import annotations
import os
from typing import Optional
from resources import with_parent
from .child import Child
import resources


class Parent(Child):
    def __init__(
            self,
            has_files: bool,
            parent: Optional[Parent] = None,
            **kwargs,
    ):
        super().__init__(parent=parent, **kwargs)
        self.children: list[Child] = []
        self.has_files = has_files

    def __enter__(self):
        with_parent.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with_parent.pop()

    @property
    def all(self) -> list:
        all = [self]
        for child in sorted(self.children):
            if hasattr(child, 'all'):
                all += child.all
            else:
                all.append(child)
        return all

    @property
    def url(self) -> str:
        dir_parts = self.dir_parts()
        return ('/' + '/'.join(dir_parts) + '/') if dir_parts else '/'

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
                                resources.links_file.LinksFile(source, self)
                            else:
                                resources.file.File(source, self)
        for child in self.children:
            if hasattr(child, 'find_files'):
                child.find_files(source_dir)

    def should_include_file(self, name: str) -> bool:
        return not name.startswith('.')
