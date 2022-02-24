from collections import defaultdict
from typing import List

from bs4.element import Tag, PageElement, NavigableString


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
