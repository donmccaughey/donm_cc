from bs4 import BeautifulSoup
from bs4.element import Tag, PageElement, NavigableString
from collections import defaultdict
from typing import List


class ContentReport:
    def __init__(self, nodes: List[PageElement]):
        self.page_element_count = len(nodes)
        self.text_nodes = 0
        self.elements = 0
        self.element_counts = defaultdict(int)
        self.blocks = 0
        self.block_counts = defaultdict(int)
        self.inlines = 0
        self.inline_counts = defaultdict(int)
        self.others = 0
        self.other_counts = defaultdict(int)

        for node in nodes:
            if isinstance(node, NavigableString):
                self.text_nodes += 1
            else:
                assert isinstance(node, Tag)
                self.elements += 1
                self.element_counts[node.name] += 1
                if node.name in ['div', 'ol', 'p', 'pre', 'table', 'ul']:
                    self.blocks += 1
                    self.block_counts[node.name] += 1
                elif node.name in ['a', 'b', 'code', 'em', 'i', 'span', 'strong', 'u']:
                    self.inlines += 1
                    self.inline_counts[node.name] += 1
                else:
                    self.others += 1
                    self.other_counts[node.name] += 1

    def print_statistics(self, brief=True):
        if brief:
            s = f'    {self.page_element_count} page elements ['
            parts = []
            for name, count in sorted(self.element_counts.items()):
                parts.append(f'{name}: {count}')
            parts.append(f'text: {self.text_nodes}')
            s += ', '.join(parts)
            s += ']'
            print(s)
        else:
            print(f'    {self.page_element_count} page elements')
            print(f'        {self.text_nodes} text nodes')
            print(f'        {self.blocks} block tags')
            if not brief:
                for key in sorted(self.block_counts.keys()):
                    print(f'            {key}: {self.block_counts[key]}')
            print(f'        {self.inlines} inline tags')
            if not brief:
                for key in sorted(self.inline_counts.keys()):
                    print(f'            {key}: {self.inline_counts[key]}')
            print(f'        {self.others} other tags')
            if not brief:
                for key in sorted(self.other_counts.keys()):
                    print(f'            {key}: {self.other_counts[key]}')


class Content:
    def __init__(self, document: BeautifulSoup):
        self.document = document
        self.nodes = extract_children(self.document.body)
        self.report = ContentReport(self.nodes)

        self.nodes = make_paragraphs(self.document, self.nodes)
        self.nodes = clean_div_tags(self.nodes)
        self.nodes = clean_pre_tags(self.nodes)
        self.nodes = clean_pre_tags(self.nodes)

    def __iter__(self):
        return iter(self.nodes)


def clean_div_tags(nodes: List[PageElement]) -> List[PageElement]:
    new_nodes = []
    for node in nodes:
        if is_tag(node, 'div'):
            div_contents = extract_children(node)
            strip_br_tags(div_contents)
            node.extend(div_contents)
        new_nodes.append(node)
    return new_nodes


def clean_pre_tags(nodes: List[PageElement]) -> List[PageElement]:
    new_nodes = []
    for node in nodes:
        if is_tag(node, 'pre'):
            pre_contents = extract_children(node)
            br_tags_to_new_lines(pre_contents)
            node.extend(pre_contents)
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


def br_tags_to_new_lines(nodes: List[PageElement]):
    for i in range(len(nodes)):
        if is_tag(nodes[i], 'br'):
            nodes[i] = '\n'


def strip_br_tags(nodes: List[PageElement]):
    while nodes and is_tag(nodes[0], 'br'):
        del nodes[0]
    while nodes and is_tag(nodes[-1], 'br'):
        del nodes[-1]
