import os
from typing import Optional

from gen import Child, Parent


class File(Child):
    def __init__(
            self,
            source: str,
            parent: Optional[Parent]=None,
            **kwargs,
    ):
        super().__init__(
            name=os.path.basename(source),
            parent=parent,
            **kwargs,
        )
        self.source = source

    def write_tree_description(self, f):
        f.write(f'{self.path}\n')
