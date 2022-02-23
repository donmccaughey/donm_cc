from datetime import datetime
from typing import List, Optional
from xml.etree.ElementTree import Element
from . import NAMESPACES


def get_author(entry: Element) -> str:
    name = entry.find('./atom:author/atom:name', NAMESPACES)
    return name.text


def get_categories(entry: Element) -> List[str]:
    category_tags = entry.findall('./atom:category', NAMESPACES)
    categories = []
    for tag in category_tags:
        if tag.get('scheme') == 'http://www.blogger.com/atom/ns#':
            categories.append(tag.get('term'))
    return categories


def get_content(entry: Element) -> str:
    content = entry.find('./atom:content', NAMESPACES)
    return content.text


def get_kind(entry: Element) -> str:
    category_tags = entry.findall('./atom:category', NAMESPACES)
    kinds = []
    for tag in category_tags:
        if tag.get('scheme') == 'http://schemas.google.com/g/2005#kind':
            term = tag.get('term')
            category = term.split('#')[1]
            kinds.append(category)
    assert len(kinds) == 1
    return kinds[0]


def get_title(entry: Element) -> str:
    title = entry.find('./atom:title', NAMESPACES)
    return title.text


def get_original_url(entry: Element) -> Optional[str]:
    link_tags = entry.findall('./atom:link', NAMESPACES)
    alternate_links = [tag for tag in link_tags if tag.get('rel') == 'alternate']
    return alternate_links[0].get('href') if len(alternate_links) else None


def get_published(entry: Element) -> datetime:
    published = entry.find('./atom:published', NAMESPACES)
    return datetime.fromisoformat(published.text)


def get_updated(entry: Element) -> str:
    updated = entry.find('./atom:updated', NAMESPACES)
    return updated.text


class Entry:
    def __init__(self, element):
        self.element = element

        self.author = get_author(self.element)
        self.categories = get_categories(self.element)
        self.content = get_content(self.element)
        self.kind = get_kind(self.element)
        self.original_url = get_original_url(self.element)
        self.title = get_title(self.element)
        self.published = get_published(self.element)
        self.updated = get_updated(self.element)
