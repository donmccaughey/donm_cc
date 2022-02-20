import os

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from datetime import datetime
from typing import List, Optional
from xml.etree.ElementTree import Element
from . import NAMESPACES


HTML_START = '''<!doctype html>
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content='initial-scale=0.9, width=device-width'>
'''


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

    def make_new_filename(self) -> str:
        year = self.published.year
        month = self.published.month
        day = self.published.day

        title = self.title.lower()
        title = title.replace('objective-c tuesdays: ', '')
        title = title.replace('@', 'at-')
        title = title.replace('...', '-')
        title = title.replace(',', '')
        title = title.replace(' ', '_')
        return f'{year:04}-{month:02}-{day:02}-{title}.html'

    def save(self, output_dir: str):
        path = os.path.join(output_dir, self.make_new_filename())
        with open(path, 'w') as f:
            self.write_document(f)

    def write_document(self, f):
        f.write('<!doctype html>\n')
        f.write('<html lang=en>\n')
        self.write_head(f)
        self.write_body(f)

    def write_head(self, f):
        f.write('<meta charset=utf-8>\n')
        f.write("<meta name=viewport content='initial-scale=0.9, width=device-width'>\n")
        f.write(f'<title>{self.title}</title>\n')

    def write_body(self, f):
        soup = BeautifulSoup(self.content, 'html5lib')
        add_h1(soup, self.title)
        add_new_lines_after_blocks(soup)
        convert_br_to_new_line_in_pre_tags(soup)
        add_new_lines_around_br_tags(soup)
        for child in soup.body.children:
            f.write(str(child))
        f.write('\n')


def add_h1(soup: BeautifulSoup, title: str):
    h1 = soup.new_tag('h1')
    h1.append(title)
    soup.body.insert(0, '\n')
    soup.body.insert(0, h1)


def add_newline_after(tag: Tag):
    if (
            not isinstance(tag.next_sibling, NavigableString)
            or not tag.next_sibling.startswith('\n')
    ):
        tag.insert_after('\n')


def add_newline_before(tag: Tag):
    if (
            not isinstance(tag.previous_sibling, NavigableString)
            or not tag.previous_sibling.startswith('\n')
    ):
        tag.insert_before('\n')


def add_new_lines_after_blocks(soup: BeautifulSoup):
    for div in soup.find_all('div'):
        add_newline_after(div)
    for div in soup.find_all('pre'):
        add_newline_after(div)


def convert_br_to_new_line_in_pre_tags(soup: BeautifulSoup):
    for pre in soup.find_all('pre'):
        br_tags = pre.find_all('br')
        for br in br_tags:
            br.replace_with('\n')


def add_new_lines_around_br_tags(soup: BeautifulSoup):
    for br in soup.find_all('br'):
        add_newline_before(br)
        add_newline_after(br)
