from typing import Optional

from gen import Parent
from gen.page import Page


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
