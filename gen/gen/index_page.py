from typing import Optional

from gen import Parent
from gen.page import Page


class IndexPage(Parent, Page):
    def __init__(
            self,
            title: str,
            parent: Optional[Parent]=None,
            name: Optional[str] = None,
            is_root: bool = False,
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
        self.is_root = is_root

    @property
    def dir_parts(self) -> list[str]:
        return (
                (self.parent.dir_parts if self.parent else ['.'])
                + ([] if self.is_root else [self.name])
        )

    @property
    def file_parts(self) -> list[str]:
        return ['index.html']

    def should_include_file(self, name: str) -> bool:
        if name in ['index.html']:
            return False
        else:
            return super().should_include_file(name)

    def write_tree_description(self, f):
        super().write_tree_description(f)
        for child in self.children:
            child.write_tree_description(f)
