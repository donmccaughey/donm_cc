import os
from typing import Optional

from site import Parent


class Directory(Parent):
    def __init__(
            self,
            name: str,
            parent: Optional[Parent]=None,
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
    def dir_parts(self) -> list[str]:
        return (self.parent.dir_parts if self.parent else []) + [self.name]

    @property
    def file_parts(self) -> list[str]:
        return []

    @property
    def path(self) -> str:
        return './' + self.dirname

    def generate(self, output_path: str, is_dry_run: bool=True):
        path = os.path.join(output_path, self.path)
        path = os.path.normpath(path)
        print('creating directory', path)
        if not is_dry_run:
            os.makedirs(path, exist_ok=False)
        for child in self.children:
            child.generate(output_path, is_dry_run)
