from typing import Optional

from gen import Child, Parent


def make_name(title: str):
    lowered = title.lower()
    return lowered.replace(' ', '_')


class Page(Child):
    def __init__(
            self,
            title: str,
            parent: Parent,
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
    def filename(self) -> Optional[str]:
        return self.name + '.html'

    def write_tree_description(self, f):
        f.write(f'{self.path} "{self.title}"\n')
