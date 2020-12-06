from typing import Optional

from gen import Parent


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
        return (self.parent.dir_parts if self.parent else ['.']) + [self.name]

    @property
    def file_parts(self) -> list[str]:
        return []

    @property
    def path(self) -> str:
        return self.dirname

    def write_tree_description(self, f):
        f.write(f'{self.dirname}\n')
        for child in self.children:
            child.write_tree_description(f)
