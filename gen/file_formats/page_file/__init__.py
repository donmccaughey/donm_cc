from dataclasses import dataclass
from typing import Optional, List


@dataclass
class BookLink:
    modifier: str
    title: str
    link: Optional[str]
    authors: List[str]
    date: Optional[str]
    checked: bool


@dataclass
class Link:
    modifier: str
    title: str
    link: Optional[str]
    authors: List[str]
    date: Optional[str]
    checked: bool


@dataclass
class LinksSection:
    title: str
    notes: list[str]
    links: list[BookLink | Link]


@dataclass
class PageFile:
    title: str
    notes: list[str]
    sections: list[LinksSection]
