import os

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag, PageElement
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
        f.write('<link rel=stylesheet href=/base.css>\n')

    def write_body(self, f):
        soup = BeautifulSoup(self.content, 'html5lib')
        contents = extract_body_contents(soup)

        add_nav(soup)
        section = add_section(soup, self.title, contents)
        clean_up_div_tags(soup, section)
        clean_up_pre_tags(soup, section)
        clean_up_paragraphs(soup, section)
        for child in soup.body.contents:
            f.write(str(child))


def extract_body_contents(soup: BeautifulSoup) -> List[PageElement]:
    node = soup.body.contents[0]
    contents = [node]
    while node.next_sibling:
        node = node.next_sibling
        contents.append(node)
    for node in contents:
        node.extract()
    return contents


def add_nav(soup: BeautifulSoup):
    nav = soup.new_tag('nav')
    nav.append('\n    ')
    a = soup.new_tag('a')
    a['href'] = '/'
    a.append('Don McCaughey')
    nav.append(a)

    nav.append(' • ')

    a = soup.new_tag('a')
    a['href'] = '/objective-c_tuesdays/'
    a.append('Objective-C Tuesdays')
    nav.append(a)
    nav.append('\n')

    soup.body.insert(0, nav)
    soup.body.insert(1, '\n')


def add_section(soup: BeautifulSoup, title: str, contents: List[PageElement]) -> Tag:
    section = soup.new_tag('section')
    soup.body.append(section)
    soup.body.append('\n')

    section.append('\n')
    h1 = soup.new_tag('h1')
    h1.append(title)
    section.append(h1)
    section.append('\n')

    section.extend(contents)
    section.append('\n')

    return section


def clean_up_div_tags(soup: BeautifulSoup, section: Tag):
    # TODO: clean up "See Also" boxes
    for div in section.find_all('div'):
        add_newline_after(div)
        div.insert(0, '\n    ')
        div.append('\n')


def clean_up_pre_tags(soup: BeautifulSoup, section: Tag):
    for pre in section.find_all('pre'):
        add_newline_before(pre)
        add_newline_after(pre)
        br_tags = pre.find_all('br')
        for br in br_tags:
            br.replace_with('\n')


def clean_up_paragraphs(soup: BeautifulSoup, section: Tag):
    clean_up_double_br_paragraphs(soup, section)

    highlight_br_tags(section)

    clean_up_text_between_blocks(soup, section)
    convert_bold_section_titles_to_headers(soup, section)


def clean_up_double_br_paragraphs(soup: BeautifulSoup, section: Tag):
    br_groups = []
    brs = []
    for child in section.children:
        if isinstance(child, Tag) and child.name == 'br':
            brs.append(child)
        else:
            if brs and len(brs) > 1:
                br_groups.append(brs)
            brs = []
    if brs and len(brs) > 1:
        br_groups.append(brs)

    for brs in br_groups:
        brs[0].insert_before('\n')
        p = soup.new_tag('p')
        p.append('\n    ')
        brs[0].insert_before(p)

        while is_paragraph_content(brs[-1].next_sibling):
            node = brs[-1].next_sibling.extract()
            p.append(node)
        p.append('\n')

        for br in brs:
            br.extract()


def clean_up_text_between_blocks(soup: BeautifulSoup, section: Tag):
    # TODO: find content between <div>, <pre> and <p> tags
    pass


def convert_bold_section_titles_to_headers(soup: BeautifulSoup, section: Tag):
    pass


def is_paragraph_content(node: PageElement) -> bool:
    if not node:
        return False
    if isinstance(node, Tag):
        tag: Tag = node
        return tag.name not in ['br', 'div', 'p', 'pre']
    if isinstance(node, NavigableString):
        return str(node) != '\n' or node.next_sibling is not None
    return True


def add_newline_after(tag: Tag):
    if (
            not isinstance(tag.next_sibling, NavigableString)
            or not tag.next_sibling.startswith('\n')
    ):
        tag.insert_after('\n')


def add_newline_before(tag: Tag):
    if (
            not isinstance(tag.previous_sibling, NavigableString)
            or not tag.previous_sibling.endswith('\n')
    ):
        tag.insert_before('\n')


def highlight_br_tags(section: Tag):
    for child in section.contents:
        if isinstance(child, Tag) and child.name == 'br':
            add_newline_before(child)
            add_newline_after(child)
