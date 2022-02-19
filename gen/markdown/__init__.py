from __future__ import annotations
from typing import Optional

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from markup import A, Code, Em, Node, P, Strong, Text

md = MarkdownIt()


def note_to_markup(note: str, parent: Optional[Node] = None) -> P:
    stack = [(P(parent=parent))]
    root = SyntaxTreeNode(md.parseInline(note))
    for node in root.walk(include_self=False):
        if node.level < len(stack) - 1:
            stack.pop()
        parent = stack[-1]
        match node.type:
            case 'code_inline':
                Code(text=node.content, parent=parent)
            case 'em':
                stack.append(Em(parent=parent))
            case 'html_inline':
                print(f'WARNING: inline HTML in Markdown')
                print(f'>>> {note}')
                print()
            case 'inline':
                pass
            case 'link':
                href = node.attrs['href']
                stack.append(A(href=href, parent=parent))
            case 'softbreak':
                Text(' ', parent=parent)
            case 'strong':
                stack.append(Strong(parent=parent))
            case 'text':
                Text(node.content, parent=parent)
            case _:
                print(f'WARNING: unexpected Markdown {node.type}')
                print(f'>>> {note}')
                print()
    return stack[0]
