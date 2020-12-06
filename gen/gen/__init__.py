from __future__ import annotations

import os
from typing import Optional


class Child:
    def __init__(self, name: str, parent: Optional[Parent], **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.parent = parent
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
    def __init__(self, parent: Optional[Parent], has_files: bool, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.children: list[Child] = []
        self.has_files = has_files

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


class File(Child):
    def __init__(
            self,
            source: str,
            parent: Parent,
            **kwargs,
    ):
        super().__init__(
            name=os.path.basename(source),
            parent=parent,
            **kwargs,
        )
        self.source = source

    def write_tree_description(self, f):
        f.write(f'{self.path}\n')


class Directory(Parent):
    def __init__(
            self,
            name: str,
            parent: Parent,
            has_files: bool = True,
            **kwargs,
    ):
        super().__init__(
            has_files=has_files,
            name=name,
            parent=parent,
            **kwargs,
        )

    @property
    def dirname(self) -> str:
        return self.parent.dirname + self.name + '/'

    @property
    def filename(self) -> Optional[str]:
        return None

    def write_tree_description(self, f):
        f.write(f'{self.dirname}\n')
        for child in self.children:
            child.write_tree_description(f)


def make_name(title: str):
    lowered = title.lower()
    return lowered.replace(' ', '_')


class Page(Child):
    def __init__(
            self,
            title: str,
            parent: Parent,
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
    def filename(self) -> Optional[str]:
        return self.name + '.html'

    def write_tree_description(self, f):
        f.write(f'{self.path} "{self.title}"\n')


class IndexPage(Parent, Page):
    def __init__(
            self,
            title: str,
            parent: Optional[Parent],
            name: Optional[str] = None,
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
        self.has_files = has_files

    @property
    def dirname(self) -> str:
        return (self.parent.dirname + self.name + '/') if self.parent else './'

    @property
    def filename(self) -> Optional[str]:
        return 'index.html'

    def should_include_file(self, name: str) -> bool:
        if name in ['index.html']:
            return False
        else:
            return super().should_include_file(name)

    def write_tree_description(self, f):
        super().write_tree_description(f)
        for child in self.children:
            child.write_tree_description(f)
