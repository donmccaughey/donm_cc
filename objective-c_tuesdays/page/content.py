from typing import List, Dict

from bs4 import BeautifulSoup
from bs4.element import Tag, PageElement

from page.content_report import ContentReport


class Content:
    def __init__(self, document: BeautifulSoup, url_map: Dict[str, str]):
        self.document = document
        self.url_map = url_map

        self.nodes = extract_children(self.document.body)
        self.report = ContentReport(self.nodes)

        self.nodes = remove_style_tags(self.nodes)
        self.nodes = make_paragraphs(self.document, self.nodes)
        self.nodes = clean_a_tags(self.nodes, self.url_map)
        self.nodes = clean_div_tags(self.nodes)
        self.nodes = clean_pre_tags(self.nodes)

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
        if is_tag(node, 'div'):
            div_contents = extract_children(node)
            strip_br_tags(div_contents)
            node.extend(div_contents)
            if 'seeAlsoBox' in node['class']:
                node.name = 'aside'
                del node['class']
        new_nodes.append(node)
    return new_nodes


def clean_pre_tags(nodes: List[PageElement]) -> List[PageElement]:

    def br_tags_to_new_lines(element: Tag):
        for child in element.children:
            if isinstance(child, Tag):
                if child.name == 'br':
                    child.replace_with('\n')
                else:
                    br_tags_to_new_lines(child)

    new_nodes = []
    for node in nodes:
        if is_tag(node, 'pre'):
            pre: Tag = node
            br_tags_to_new_lines(pre)
            remove_class(pre, 'prettyprint')
        new_nodes.append(node)
    return new_nodes


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
    paragraphs = [[]]
    i = 0
    while i < len(nodes):
        # TODO: handle runs of 3+ <br> tags
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
