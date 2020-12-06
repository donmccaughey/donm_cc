import os
import shutil
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

    def generate(self, output_path: str, is_dry_run=True):
        path = os.path.join(output_path, self.path)
        path = os.path.normpath(path)
        print('copying file', path, 'from source', self.source)
        if not is_dry_run:
            if os.path.exists(path):
                raise FileExistsError
            shutil.copyfile(self.source, path, follow_symlinks=True)

    def find_files(self, source_dir: str):
        path = os.path.join(os.getcwd(), source_dir)
        path = os.path.join(path, self.source)
        path = os.path.normpath(path)
        self.source = os.path.relpath(path)
        if not os.path.exists(self.source):
            raise FileNotFoundError
