from bs4 import Tag, PageElement, NavigableString

from page import Page


class PageFile:
    def __init__(self, page: Page):
        self.page = page

    def __str__(self) -> str:
        lines = [
            f'.page essay {self.page.title}',
            '',
        ]
        for node in self.page.content.nodes:
            if not isinstance(node, Tag):
                raise RuntimeError(f'Unexpected node {node}')
            tag: Tag = node
            match tag.name:
                case 'h2':
                    lines.append('')
                    lines.append(h2_to_markdown(tag))
                    lines.append('')
                case 'ol':
                    lines.append(str(tag))
                case 'p':
                    lines.extend(p_to_markdown(tag))
                    lines.append('')
                case 'pre':
                    lines.extend(pre_to_markdown(tag))
                    lines.append('')
                case 'table':
                    lines.append(str(tag))
                case 'ul':
                    lines.append(str(tag))
                case _:
                    raise RuntimeError(f'Unexpected tag {tag.name}')
        return '\n'.join(lines)


def h2_to_markdown(h2: Tag) -> str:
    return f'## {h2.text}'


def p_to_markdown(p: Tag) -> list[str]:
    # TODO: handle child tags recursively
    text = ''
    for node in p.children:
        if isinstance(node, NavigableString):
            text += node.text
        elif isinstance(node, Tag):
            tag: Tag = node
            match tag.name:
                case 'a':
                    text += f'[{tag.text}]({tag.attrs["href"]})'
                case 'b':
                    text += f'**{tag.text}**'
                case 'br':
                    text += '\n'
                case 'code':
                    text += f'`{tag.text}`'
                case 'em':
                    text += f'_{tag.text}_'
                case 'mark':
                    text += f'<mark>{tag.text}</mark>'
                case 'span':
                    text += f'{tag.text}'
                case 'strong':
                    text += f'**{tag.text}**'
                case _:
                    raise RuntimeError(f'Unexpected tag {tag.name}')
    return wrap(text)


def pre_to_markdown(pre: Tag) -> list[str]:
    # TODO: handle child tags recursively
    lines = pre.text.splitlines()
    return [f'    {line}' for line in lines]


def wrap(text: str, width=80) -> list[str]:
    lines = []
    words = text.split()
    line = ''
    line_width = 0
    while words:
        word = words[0]
        word_width = len(word)
        if line:
            space_width = 2 if line.endswith('.') else 1
            if (line_width + space_width + word_width) > width:
                lines.append(line)
                line = ''
                line_width = 0
            else:
                space = '  ' if space_width == 2 else ' '
                line += (space + word)
                line_width += (space_width + word_width)
                words.pop(0)
        else:
            line += word
            line_width += word_width
            words.pop(0)
    lines.append(line)
    return lines
