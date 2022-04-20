from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Callable, Tuple
from . import with_parent

if TYPE_CHECKING:
    from .directory import Directory


class Resource:
    def __init__(
            self,
            name: str,
            parent: Optional[Directory] = None,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.name = name
        self.parent = parent if parent else with_parent[-1]
        if self.parent:
            self.parent.children.append(self)

    def __iter__(self):
        yield self

    def __lt__(self, other: Resource) -> bool:
        return self.path_parts() < other.path_parts()

    def find_directories(self) -> list[Directory]:
        directories = []
        parent = self.parent
        while parent:
            directories.insert(0, parent)
            parent = parent.parent
        return directories

    def find_links(self) -> list[Tuple[Resource, str]]:
        return []

    @property
    def dirname(self) -> str:
        dir_parts = self.dir_parts()
        return ('/'.join(dir_parts) + '/') if dir_parts else './'

    def dir_parts(self) -> list[str]:
        return self.parent.dir_parts() if self.parent else []

    @property
    def filename(self) -> Optional[str]:
        file_parts = self.file_parts()
        return file_parts[0] if file_parts else None

    def file_parts(self) -> list[str]:
        return [self.name]

    @property
    def path(self) -> str:
        path_parts = self.path_parts()
        return ('./' + '/'.join(path_parts)) if path_parts else './'

    def path_parts(self) -> list[str]:
        return self.dir_parts() + self.file_parts()

    @property
    def url(self) -> str:
        path_parts = self.path_parts()
        return ('/' + '/'.join(path_parts)) if path_parts else '/'

    def build_documents(self):
        raise NotImplementedError

    def generate(
            self,
            output_path: str,
            is_dry_run=True,
            overwrite=False,
    ):
        raise NotImplementedError
