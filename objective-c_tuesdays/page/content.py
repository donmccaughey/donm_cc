from bs4 import BeautifulSoup
from bs4.element import Tag, PageElement

from typing import List


class Content:
    def __init__(self, document: BeautifulSoup):
        self.document = document
        self.content = extract_contents(self.document.body)
        self.content = make_paragraphs(self.document, self.content)
        # TODO: <div> and <pre> cleanup

    def __iter__(self):
        return iter(self.content)


def make_paragraphs(document: BeautifulSoup, content: List[PageElement]) -> List[PageElement]:
    new_content = []
    for block in split_blocks(content):
        if isinstance(block, Tag):
            new_content.append(block)
        else:
            paragraphs = split_paragraphs(block)
            p_tags = [to_p(document, paragraph) for paragraph in paragraphs]
            new_content.extend(p_tags)
    return new_content


def extract_contents(element: Tag) -> List[PageElement]:
    contents = list(element.children)
    for node in contents:
        node.extract()
    return contents


def is_block(node: PageElement) -> bool:
    return (
            isinstance(node, Tag)
            and node.name in ['div', 'ol', 'p', 'pre', 'table', 'ul']
    )


def is_br(node: PageElement) -> bool:
    return isinstance(node, Tag) and node.name == 'br'


def to_p(document: BeautifulSoup, paragraph: List[PageElement]) -> Tag:
    strip_br_tags(paragraph)
    p = document.new_tag('p')
    p.extend(paragraph)
    return p


def split_blocks(contents: List[PageElement]) -> List[Tag | List[PageElement]]:
    blocks = []
    inline = []
    for node in contents:
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


def split_paragraphs(inline: List[PageElement]) -> List[List[PageElement]]:
    paragraphs = [[]]
    i = 0
    while i < len(inline):
        # TODO: handle runs of 3+ <br> tags
        node1 = inline[i]
        node2 = inline[i + 1] if i < len(inline) - 1 else None
        if is_br(node1) and node2 and is_br(node2):
            paragraphs.append([])
            i += 1
        else:
            paragraphs[-1].append(node1)
        i += 1
    return paragraphs


def strip_br_tags(contents: List[PageElement]):
    while contents and is_br(contents[0]):
        del contents[0]
    while contents and is_br(contents[-1]):
        del contents[-1]
