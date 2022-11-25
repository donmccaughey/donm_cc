from dataclasses import dataclass
from typing import Optional, List


@dataclass
class BookLink:
    modifier: str
    title: str  # markdown
    asin: Optional[str]
    olw: Optional[str]
    url: Optional[str]
    authors: List[str]
    date: Optional[str]
    checked: bool


@dataclass
class Link:
    modifier: str
    title: str  # markdown
    url: Optional[str]
    authors: List[str]
    date: Optional[str]
    checked: bool


@dataclass
class LinksSection:
    title: str
    notes: List[str]  # markdown
    links: List[BookLink | Link]


@dataclass
class PageFile:
    modifier: str
    title: str
    subtitle: Optional[str]
    notes: List[str]  # markdown
    sections: List[LinksSection]

    @property
    def full_title(self) -> str:
        return f'{self.title}: {self.subtitle}' if self.subtitle else self.title
