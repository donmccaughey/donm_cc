import os
from typing import Optional

from .name_mixin import NameMixin
from .parent import Parent


class Directory(NameMixin, Parent):
    def __init__(
            self,
            name: str,
            parent: Optional[Parent] = None,
            is_root: bool = False,
            has_files: bool = True,
            **kwargs,
    ):
        super().__init__(
            has_files=has_files,
            name=name,
            parent=parent,
            **kwargs,
        )
        self.is_root = is_root

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
