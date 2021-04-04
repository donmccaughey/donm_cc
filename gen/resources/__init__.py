from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .parent import Parent


with_parent: list[Optional[Parent]] = [None]


from .directory import Directory
from .file import File
from .links_file import LinksFile
from .page import Page
