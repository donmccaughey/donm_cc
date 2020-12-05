from __future__ import annotations

import os
import sys
from typing import Optional, Union


def make_name(title: str):
    lowered = title.lower()
    unspaced = lowered.replace(' ', '_')
    return unspaced


class File:
    def __init__(self, source: str, parent: Union[Directory, IndexPage]):
        self.name = os.path.basename(source)
        self.parent = parent
        self.source = source
        parent.children.append(self)

    @property
    def path(self) -> str:
        return self.parent.dir + self.name

    @property
    def rank(self) -> int:
        return self.parent.rank + 1 if self.parent else 0

    def write_tree_description(self, f):
        f.write(f'{self.path}\n')


class Directory:
    def __init__(self, name: str, parent: Union[Directory, IndexPage], has_files: bool = True):
        self.children: list[Union[File, Directory]] = []
        self.name = name
        self.parent = parent
        self.has_files = has_files
        parent.children.append(self)

    @property
    def dir(self) -> str:
        return self.parent.dir + self.name + '/'

    @property
    def path(self) -> str:
        return self.dir

    @property
    def rank(self) -> int:
        return self.parent.rank + 1 if self.parent else 0

    def find_files(self, source_dir: str):
        path = os.path.join(os.getcwd(), source_dir)
        path = os.path.join(path, self.dir)
        path = os.path.normpath(path)
        if self.has_files:
            with os.scandir(path) as dir:
                for entry in dir:
                    if entry.is_file():
                        if entry.name.startswith('.'):
                            continue
                        source = os.path.join(path, entry.name)
                        file = File(source, self)
        for child in self.children:
            if hasattr(child, 'find_files'):
                child.find_files(source_dir)

    def should_include_file(self, name: str) -> bool:
        if name.startswith('.'):
            return False
        return True

    def write_tree_description(self, f):
        f.write(f'{self.path}\n')
        for child in self.children:
            child.write_tree_description(f)


class Page:
    def __init__(self, title: str, parent: Optional[IndexPage], name: Optional[str] = None):
        self.name = name if name is not None else make_name(title)
        self.title = title
        self.parent = parent
        if parent:
            parent.children.append(self)

    @property
    def path(self) -> str:
        return self.parent.dir + self.name + '.html'

    @property
    def rank(self) -> int:
        return self.parent.rank + 1 if self.parent else 0

    def write_tree_description(self, f):
        f.write(f'{self.path} "{self.title}"\n')


class IndexPage(Page):
    def __init__(self, title: str, parent: Optional[IndexPage], name: Optional[str] = None, has_files: bool = False):
        super().__init__(title, parent, name)
        self.children: list[Union[Directory, File, Page]] = []
        self.has_files = has_files

    @property
    def dir(self) -> str:
        if self.parent:
            return self.parent.dir + self.name + '/'
        else:
            return './'

    @property
    def path(self) -> str:
        return self.dir + 'index.html'

    def find_files(self, source_dir: str):
        path = os.path.join(os.getcwd(), source_dir)
        path = os.path.join(path, self.dir)
        path = os.path.normpath(path)
        if self.has_files:
            with os.scandir(path) as dir:
                for entry in dir:
                    if entry.is_file() and self.should_include_file(entry.name):
                        source = os.path.join(path, entry.name)
                        file = File(source, self)
        for child in self.children:
            if hasattr(child, 'find_files'):
                child.find_files(source_dir)

    def should_include_file(self, name: str) -> bool:
        if name.startswith('.'):
            return False
        if name in ['index.html']:
            return False
        return True

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
