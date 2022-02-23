import os

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag, PageElement
from collections import defaultdict
from datetime import datetime
from typing import List, Optional
from xml.etree.ElementTree import Element
from . import NAMESPACES


BLOCK_TAGS = ['div', 'ol', 'p', 'pre', 'table', 'ul']


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

    def report_on_contents(self, contents: List[PageElement]):
        print(self.title)
        print(f'    {len(contents)} page elements')

        text_nodes = 0
        blocks = 0
        block_counts = defaultdict(int)
        inlines = 0
        inline_counts = defaultdict(int)
        others = 0
        other_counts = defaultdict(int)

        for element in contents:
            if isinstance(element, NavigableString):
                text_nodes += 1
            else:
                assert isinstance(element, Tag)
                if element.name in BLOCK_TAGS:
                    blocks += 1
                    block_counts[element.name] += 1
                elif element.name in ['a', 'b', 'code', 'em', 'i', 'span', 'strong', 'u']:
                    inlines += 1
                    inline_counts[element.name] += 1
                else:
                    others += 1
                    other_counts[element.name] += 1

        print(f'    {text_nodes} text nodes')
        print(f'    {blocks} block tags')
        for key in sorted(block_counts.keys()):
            print(f'        {key}: {block_counts[key]}')
        print(f'    {inlines} inline tags')
        for key in sorted(inline_counts.keys()):
            print(f'        {key}: {inline_counts[key]}')
        print(f'    {others} other tags')
        for key in sorted(other_counts.keys()):
            print(f'        {key}: {other_counts[key]}')
