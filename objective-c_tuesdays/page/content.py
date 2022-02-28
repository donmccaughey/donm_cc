from typing import List, Dict

from bs4 import BeautifulSoup
from bs4.element import Tag, PageElement, NavigableString

from page.content_report import ContentReport


class Content:
    def __init__(self, document: BeautifulSoup, url_map: Dict[str, str]):
        self.document = document
        self.url_map = url_map

        self.nodes = extract_children(self.document.body)
        self.report = ContentReport(self.nodes)

        self.nodes = remove_style_tags(self.nodes)
        self.nodes = make_paragraphs(self.document, self.nodes)
        self.nodes = promote_subsection_headers(self.nodes)
        self.nodes = clean_a_tags(self.nodes, self.url_map)
        self.nodes = clean_div_tags(self.nodes)
        self.nodes = clean_pre_tags(self.nodes)
        self.nodes = clean_p_tags(self.nodes)
        self.nodes = transform_i_tags(self.nodes)
        self.nodes = transform_u_tags(self.nodes)

    def __iter__(self):
        return iter(self.nodes)


def clean_a_tags(nodes: List[PageElement], url_map: Dict[str, str]) -> List[PageElement]:
    for node in nodes:
        if isinstance(node, Tag):
            if node.name == 'a':
                a: Tag = node
                del a['target']
                href = a['href']
                if href in url_map:
                    a['href'] = url_map[href]
            clean_a_tags(node.contents, url_map)
    return nodes


def clean_div_tags(nodes: List[PageElement]) -> List[PageElement]:
    new_nodes = []
    for node in nodes:
        if not is_tag(node, 'div'):
            new_nodes.append(node)
    return new_nodes


def clean_pre_tags(nodes: List[PageElement]) -> List[PageElement]:
    new_nodes = []
    for node in nodes:
        if is_tag(node, 'pre'):
            pre: Tag = node
            br_tags_to_new_lines(pre)
            remove_class(pre, 'prettyprint')
            b_tags = pre.find_all('b')
            for b in b_tags:
                b.name = 'mark'
            if pre.contents and isinstance(pre.contents[0], NavigableString):
                pre.contents[0].replace_with(str(pre.contents[0]).lstrip())
            if pre.contents and isinstance(pre.contents[-1], NavigableString):
                pre.contents[-1].replace_with(str(pre.contents[-1]).rstrip())
        new_nodes.append(node)
    return new_nodes


def clean_p_tags(nodes: List[PageElement]) -> List[PageElement]:
    new_nodes = []
    for node in nodes:
        if is_tag(node, 'p'):
            p: Tag = node
            b_tags = p.find_all('b')
            for b in b_tags:
                b.name = 'strong'
        new_nodes.append(node)
    return new_nodes


def promote_subsection_headers(nodes: List[PageElement]) -> List[PageElement]:
    new_nodes = []
    for node in nodes:
        if is_tag(node, 'p'):
            p: Tag = node
            if is_tag(p.contents[0], 'b') or is_tag(p.contents[0], 'strong'):
                header = p.contents[0].extract()
                header.name = 'h2'
                new_nodes.append(header)
                strip_leading_header_junk(p)
        new_nodes.append(node)
    return new_nodes


def strip_leading_header_junk(p: Tag):
    if p.contents and isinstance(p.contents[0], NavigableString):
        s = str(p.contents[0])
        if s.startswith(':'):
            s = s[1:]
        s = s.lstrip()
        p.contents[0].replace_with(s)
    while p.contents and is_tag(p.contents[0], 'br'):
        p.contents[0].extract()


def transform_i_tags(nodes: List[PageElement]) -> List[PageElement]:
    for node in nodes:
        if is_tag(node, 'p'):
            p: Tag = node
            i_tags = p.find_all('i')
            for i in i_tags:
                i.name = 'em'
        elif is_tag(node, 'pre'):
            pre: Tag = node
            i_tags = pre.find_all('i')
            for i in i_tags:
                i.name = 'mark'
    return nodes


def transform_u_tags(nodes: List[PageElement]) -> List[PageElement]:
    for node in nodes:
        if isinstance(node, Tag):
            tag: Tag = node
            u_tags = tag.find_all('u')
            for u in u_tags:
                u.name = 'mark'
    return nodes


def remove_style_tags(nodes: List[PageElement]) -> List[PageElement]:
    new_nodes = []
    for node in nodes:
        if not is_tag(node, 'style'):
            new_nodes.append(node)
    return new_nodes


def make_paragraphs(document: BeautifulSoup, nodes: List[PageElement]) -> List[PageElement]:
    new_nodes = []
    for block in split_blocks(nodes):
        if isinstance(block, Tag):
            new_nodes.append(block)
        else:
            paragraphs = split_paragraphs(block)
            p_tags = [to_p(document, paragraph) for paragraph in paragraphs]
            new_nodes.extend(p_tags)
    return new_nodes


def extract_children(element: Tag) -> List[PageElement]:
    nodes = list(element.children)
    for node in nodes:
        node.extract()
    return nodes


def is_block(node: PageElement) -> bool:
    return (
            isinstance(node, Tag)
            and node.name in ['div', 'ol', 'p', 'pre', 'table', 'ul']
    )


def is_tag(node: PageElement, name: str) -> bool:
    return isinstance(node, Tag) and node.name == name


def br_tags_to_new_lines(element: Tag):
    for child in element.children:
        if isinstance(child, Tag):
            if child.name == 'br':
                child.replace_with('\n')
            else:
                br_tags_to_new_lines(child)


def to_p(document: BeautifulSoup, nodes: List[PageElement]) -> Tag:
    strip_br_tags(nodes)
    p = document.new_tag('p')
    p.extend(nodes)
    return p


def split_blocks(nodes: List[PageElement]) -> List[Tag | List[PageElement]]:
    blocks = []
    inline = []
    for node in nodes:
        if is_block(node):
            if inline:
                blocks.append(inline)
                inline = []
            blocks.append(node)
        else:
            inline.append(node)
    if inline:
        blocks.append(inline)
    return blocks


def split_paragraphs(nodes: List[PageElement]) -> List[List[PageElement]]:
    strip_br_tags(nodes)
    paragraphs = [[]]
    i = 0
    while i < len(nodes):
        node1 = nodes[i]
        node2 = nodes[i + 1] if i < len(nodes) - 1 else None
        if is_tag(node1, 'br') and node2 and is_tag(node2, 'br'):
            paragraphs.append([])
            i += 1
        else:
            paragraphs[-1].append(node1)
        i += 1
    return paragraphs


def remove_class(element: Tag, class_name: str):
    classes = element.get('class')
    if classes and class_name in classes:
        classes.remove(class_name)
        if len(classes):
            element['class'] = classes
        else:
            del element['class']


def strip_br_tags(nodes: List[PageElement]):
    while nodes and is_tag(nodes[0], 'br'):
        del nodes[0]
    while nodes and is_tag(nodes[-1], 'br'):
        del nodes[-1]
