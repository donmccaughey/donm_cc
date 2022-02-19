from dataclasses import dataclass
from typing import Optional, List


@dataclass
class BookLink:
    modifier: str
    title: str
    url: Optional[str]
    asin: Optional[str]
    authors: List[str]
    date: Optional[str]
    checked: bool


@dataclass
class Link:
    modifier: str
    title: str
    url: Optional[str]
    authors: List[str]
    date: Optional[str]
    checked: bool


@dataclass
class LinksSection:
    title: str
    notes: List[str]
    links: List[BookLink | Link]


@dataclass
class PageFile:
    title: str
    subtitle: Optional[str]
    notes: List[str]
    sections: List[LinksSection]

    @property
    def full_title(self) -> str:
        return f'{self.title}: {self.subtitle}' if self.subtitle else self.title
