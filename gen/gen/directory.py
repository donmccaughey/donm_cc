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
    def dirname(self) -> str:
        return self.parent.dirname + self.name + '/'

    @property
    def filename(self) -> Optional[str]:
        return None

    def write_tree_description(self, f):
        f.write(f'{self.dirname}\n')
        for child in self.children:
            child.write_tree_description(f)
