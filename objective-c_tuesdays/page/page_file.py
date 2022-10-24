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
                    lines.append(convert_h2(tag))
                    lines.append('')
                case 'ol':
                    lines.extend(convert_ol(tag))
                    lines.append('')
                case 'p':
                    lines.extend(convert_p(tag))
                    lines.append('')
                case 'pre':
                    lines.extend(convert_pre(tag))
                    lines.append('')
                case 'table':
                    lines.extend(convert_table(tag))
                    lines.append('')
                case 'ul':
                    lines.extend(convert_ul(tag))
                    lines.append('')
                case _:
                    raise RuntimeError(f'Unexpected tag {tag.name}')
        lines.append('')

        lines.append('.footer')
        lines.append('')

        title = self.page.entry.title
        href = self.page.entry.original_url
        s = f'[_{title}_]({href})'
        s += ' was originally published on '
        time = self.page.published
        s += f'<time datetime={time}>{time}</time>.'

        lines.extend(wrap(s))
        lines.append('')

        return '\n'.join(lines)


def convert_h2(h2: Tag) -> str:
    text = flatten(h2.contents)
    return f'## {text}'


def convert_list(tag: Tag, prefix: str) -> list[str]:
    lines = []
    for node in tag.contents:
        if isinstance(node, Tag) and node.name == 'li':
            li: Tag = node
            text = flatten(li.contents)
            lines.append(f'{prefix} {text}')
        else:
            raise RuntimeError(f'Unexpected node {node}')
    return lines


def convert_ol(ol: Tag) -> list[str]:
    return convert_list(ol, '1.')


def convert_p(p: Tag) -> list[str]:
    text = flatten(p.contents)
    return wrap(text)


def convert_pre(pre: Tag) -> list[str]:
    s = str(pre)
    assert s.startswith('<pre>')
    assert s.endswith('</pre>')
    s = s[5:-6]
    lines = s.splitlines()
    return [f'    {line}' for line in lines]


def convert_table(table: Tag) -> list[str]:
    # TODO: better table formatting
    s = str(table)
    assert s.startswith('<table')
    assert s.endswith('</table>')
    return s.splitlines()


def convert_ul(ul: Tag) -> list[str]:
    return convert_list(ul, '-')


def flatten(contents: list[PageElement]) -> str:
    s = ''
    for node in contents:
        match node:
            case NavigableString():
                s += node.text
            case Tag():
                tag: Tag = node
                match tag.name:
                    case 'a':
                        text = flatten(tag.contents)
                        href = tag.attrs['href']
                        s += f'[{text}]({href})'
                    case 'br':
                        s += '\n'
                    case 'code':
                        text = flatten(tag.contents)
                        s += f'`{text}`'
                    case 'em':
                        text = flatten(tag.contents)
                        s += f'_{text}_'
                    case 'mark':
                        text = flatten(tag.contents)
                        s += f'<mark>{text}</mark>'
                    case 'span':
                        text = flatten(tag.contents)
                        s += f'<span>{text}</span>'
                    case 'strong':
                        text = flatten(tag.contents)
                        s += f'**{text}**'
                    case _:
                        raise RuntimeError(f'Unexpected tag {tag.name}')
            case _:
                raise RuntimeError(f'Unexpected node {node}')
    return s


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
