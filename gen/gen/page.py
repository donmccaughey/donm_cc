import os
from typing import Optional

from gen import Child, Parent


def make_name(title: str):
    lowered = title.lower()
    return lowered.replace(' ', '_')


class Page(Child):
    def __init__(
            self,
            title: str,
            parent: Optional[Parent]=None,
            name: Optional[str] = None,
            **kwargs
    ):
        super().__init__(
            name=name if name is not None else make_name(title),
            parent=parent,
            **kwargs,
        )
        self.title = title

    @property
    def file_parts(self) -> list[str]:
        return [self.name + '.html']

    def generate(self, output_path: str, is_dry_run: bool=True):
        path = os.path.join(output_path, self.path)
        path = os.path.normpath(path)
        print('writing page', path)
        if not is_dry_run:
            with open(path, 'x', encoding='utf8') as f:
                pass
