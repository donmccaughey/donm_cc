from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Link:
    type: str
    title: str
    link: Optional[str]
    authors: Optional[str]
    authors_list: List[str]
    date: Optional[str]
    checked: bool


@dataclass
class LinksSection:
    title: str
    notes: list[str]
    links: list[Link]


@dataclass
class LinksPage:
    title: str
    notes: list[str]
    sections: list[LinksSection]
