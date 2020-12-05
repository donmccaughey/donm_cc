from __future__ import annotations

import os
import sys
from typing import Optional, Union


def make_name(title: str):
    lowered = title.lower()
    return lowered.replace(' ', '_')


class Child:
    def __init__(self, name: str, parent: Optional[Parent], **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.parent = parent
        if self.parent:
            self.parent.children.append(self)
            
    @property
    def path(self) -> str:
        return (self.parent.dir if self.parent else './') + self.name

    @property
    def rank(self) -> int:
        return self.parent.rank + 1 if self.parent else 0


class Parent(Child):
    def __init__(self, parent: Optional[Parent], has_files: bool, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.children: list[Union[File, Page, Directory]] = []
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
    def dir(self) -> str:
        raise NotImplementedError

    def find_files(self, source_dir: str):
        path = os.path.join(os.getcwd(), source_dir)
        path = os.path.join(path, self.dir)
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
    def dir(self) -> str:
        return self.path + '/'

    def write_tree_description(self, f):
        f.write(f'{self.dir}\n')
        for child in self.children:
            child.write_tree_description(f)


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
    def path(self) -> str:
        return self.parent.dir + self.name + '.html'

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
    def dir(self) -> str:
        return (self.parent.dir + self.name + '/') if self.parent else './'

    @property
    def path(self) -> str:
        return self.dir + 'index.html'

    def should_include_file(self, name: str) -> bool:
        if name in ['index.html']:
            return False
        else:
            return super().should_include_file(name)

    def write_tree_description(self, f):
        super().write_tree_description(f)
        for child in self.children:
            child.write_tree_description(f)


root = IndexPage('Don McCaughey', name="", parent=None)

aughey = IndexPage('Don McCaughey', parent=root, name='aughey')

banners = Directory('banners', parent=root)

base_css = File('base.css', parent=root)

business_novels = IndexPage('Business Novels', parent=root)

engineering_management = IndexPage('Engineering Management', parent=root)

hash_tables = IndexPage('Hash Tables', parent=root)

icons = Directory('icons', parent=root)

macos_packages = IndexPage('macOS Packages', parent=root, has_files=True)

make = IndexPage('Make', parent=root)

memory_match = IndexPage('Memory Match', parent=root, has_files=True)

random_words = IndexPage('Random Words', parent=root, has_files=True)

resume = Directory('resume', parent=root)

rust_and_wasm = IndexPage('Rust and Wasm', parent=root)

science_fiction = IndexPage('Science Fiction', parent=root)
alastair_reynolds = Page('Alastair Reynolds', parent=science_fiction)
iain_m_banks = Page('Iain M Banks', parent=science_fiction)
james_sa_corey = Page('James SA Corey', parent=science_fiction)
lois_mcmaster_bujold = Page('Lois McMaster Bujold', parent=science_fiction)


def main():
    root.find_files('../wwwroot')
    root.write_tree_description(sys.stdout)


if __name__ == '__main__':
    main()
