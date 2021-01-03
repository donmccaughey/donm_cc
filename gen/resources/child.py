from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from resources import with_parent

if TYPE_CHECKING:
    from .parent import Parent


class Child:
    def __init__(
            self,
            name: str,
            parent: Optional[Parent] = None,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.name = name
        self.parent = parent if parent else with_parent[-1]
        if self.parent:
            self.parent.children.append(self)

    def __lt__(self, other: Child) -> bool:
        return self.path_parts < other.path_parts

    @property
    def ancestors(self) -> list[Parent]:
        ancestors = []
        parent = self.parent
        while parent:
            ancestors.insert(0, parent)
            parent = parent.parent
        return ancestors

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
    def url(self) -> str:
        return ('/' + '/'.join(self.path_parts)) if self.path_parts else '/'

    def generate(self, output_path: str, is_dry_run=True, overwrite=False):
        raise NotImplementedError
