import os

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag, PageElement
from collections import defaultdict
from datetime import datetime
from typing import List, Optional
from xml.etree.ElementTree import Element
from . import NAMESPACES

HTML_START = '''<!doctype html>
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content='initial-scale=0.9, width=device-width'>
'''

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
        # self.report_on_contents(contents)

        contents = build_paragraphs(soup, contents)

        clean_up_div_tags(soup, contents)
        clean_up_pre_tags(contents)


        contents = add_linebreaks(contents)

        # TODO: remove "target='_blank'" from links
        # TODO: remove "class='prettyprint'" from <pre> tags
        # TODO: rewrite blog.ablepear.com URLs
        # TODO: find and fix draft.blogger.com URLs
        # TODO: turn leading <strong> spans into headers
        # TODO: rewrite "seeAlsoBox" as <aside>?
        # TODO: clean up tables and related style blocks
        # TODO: examine <ul> and <ol> blocks
        # TODO: survey <i>, <b> and <u> tags

        add_nav(soup)
        add_section(soup, self.title, contents)

        # TODO: add footer with link to the original

        for child in soup.body.contents:
            f.write(str(child))

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


def extract_body_contents(soup: BeautifulSoup) -> List[PageElement]:
    node = soup.body.contents[0]
    contents = [node]
    while node.next_sibling:
        node = node.next_sibling
        contents.append(node)
    for node in contents:
        node.extract()
    return contents


def is_block(node: PageElement) -> bool:
    return isinstance(node, Tag) and node.name in BLOCK_TAGS


def is_br(node: PageElement) -> bool:
    return isinstance(node, Tag) and node.name == 'br'


def inline_to_paragraphs(soup: BeautifulSoup, inline: List[PageElement]) -> List[Tag]:
    while inline and is_br(inline[0]):
        del inline[0]
    while inline and is_br(inline[-1]):
        del inline[-1]

    paragraphs = [[]]
    i = 0
    while i < len(inline):
        node1 = inline[i]
        node2 = inline[i + 1] if i < len(inline) - 1 else None
        if is_br(node1) and node2 and is_br(node2):
            paragraphs.append([])
            i += 1
        else:
            paragraphs[-1].append(node1)
        i += 1

    p_tags = []

    for paragraph in paragraphs:
        p = soup.new_tag('p')
        p.append('\n    ')
        for child in paragraph:
            p.append(child)
        p.append('\n')
        p_tags.append(p)

    return p_tags


def build_paragraphs(soup: BeautifulSoup, contents: List[PageElement]) -> List[Tag]:
    blocks = []
    inline = []
    for (i, node) in enumerate(contents):
        if is_block(node):
            if inline:
                blocks.extend(inline_to_paragraphs(soup, inline))
                inline = []
            blocks.append(node)
        else:
            inline.append(node)
    if inline:
        blocks.extend(inline_to_paragraphs(soup, inline))
    return blocks


def add_linebreaks(contents: List[Tag]) -> List[Tag]:
    with_breaks = []
    for tag in contents:
        with_breaks.append(tag)
        with_breaks.append('\n')
    return with_breaks


def get_tags_by_name(contents: List[PageElement], name: str) -> List[Tag]:
    return [
        tag for tag in contents if isinstance(tag, Tag) and tag.name == name
    ]


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
    return section


def clean_up_div_tags(soup: BeautifulSoup, contents: List[PageElement]):
    # TODO: clean up "See Also" boxes
    for div in get_tags_by_name(contents, 'div'):
        while div.contents and is_br(div.contents[-1]):
            div.contents[-1].decompose()
        div.insert(0, '\n    ')
        div.append('\n')
        for child in list(div.contents):
            if is_br(child):
                add_newline_before(child)
                add_newline_after(child)
        for child in list(div.contents):
            if isinstance(child, Tag):
                child.insert_before('    ')


def clean_up_pre_tags(contents: List[PageElement]):
    for pre in get_tags_by_name(contents, 'pre'):
        br_tags = pre.find_all('br')
        for br in br_tags:
            br.replace_with('\n')


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
