import os
from typing import Optional

from site import Parent
from site.page import Page


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
                (self.parent.dir_parts if self.parent else [])
                + ([] if self.is_root else [self.name])
        )

    @property
    def file_parts(self) -> list[str]:
        return ['index.html']

    @property
    def url(self) -> str:
        return ('/' + '/'.join(self.dir_parts) + '/') if self.dir_parts else '/'

    def generate(self, output_path: str, is_dry_run: bool=True):
        dirname = os.path.join(output_path, self.dirname)
        dirname = os.path.normpath(dirname)
        print('creating directory', dirname)
        if not is_dry_run:
            os.makedirs(dirname, exist_ok=False)
        path = os.path.join(output_path, self.path)
        path = os.path.normpath(path)
        print('writing index page', path)
        if not is_dry_run:
            with open(path, 'x', encoding='utf8') as f:
                f.write(str(self.document))
        for child in self.children:
            child.generate(output_path, is_dry_run)

    def should_include_file(self, name: str) -> bool:
        if name in ['index.html']:
            return False
        else:
            return super().should_include_file(name)
