from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .directory import Directory


with_parent: list[Optional[Directory]] = [None]


from .directory import Directory
from .file import File
from .page_file import PageFile
from .page import Page
