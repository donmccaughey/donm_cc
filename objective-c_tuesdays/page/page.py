import os
from pathlib import Path
from typing import Dict, Optional, List, Set, Tuple

from bs4 import BeautifulSoup
from bs4.element import Doctype, Tag, PageElement

from atom import Entry
from page.content import Content


class Page:
    def __init__(
            self,
            entry: Entry,
            output_dir: str,
            topic: Optional[str] = None,
            is_toc: bool = False
    ):
        self.content = None
        self.entry = entry
        self.output_dir = output_dir

        self.document = BeautifulSoup(self.entry.content, 'html5lib')
        self.filename = get_filename(self.entry)
        self.new_url = f'/objective-c_tuesdays/{self.filename}'
        self.path = os.path.join(self.output_dir, self.filename)
        self.page_path = Path(self.path).with_suffix('.page')
        self.title = get_title(self.entry)
        self.published = self.entry.published.strftime('%Y-%m-%d')
        self.topic = topic
        self.is_toc = is_toc

    def __str__(self) -> str:
        return str(self.document)

    def build(self, url_map: Dict[str, str]):
        self.content = Content(self.document, url_map)

        self.document.insert(0, Doctype('html'))
        self.document.html['lang'] = 'en'

        # head
        self.__tag(self.document.head, 'link', rel='icon', href='data:,')
        self.__tag(self.document.head, 'meta', charset='utf-8')
        self.__tag(self.document.head, 'meta', attrs={
            'name': 'viewport',
            'content': 'initial-scale=0.9, width=device-width'
        })
        self.__tag(self.document.head, 'title', text=self.title)
        self.__tag(self.document.head, 'link',
                   rel='stylesheet', href='/base.css')

        # nav
        nav = self.__tag(self.document.body, 'nav', attrs={'class': 'menu'})
        self.__tag(nav, 'a', text='Don McCaughey', href='/')
        nav.append(' • ')
        self.__tag(nav, 'a', text='Objective-C Tuesdays',
                   href='/objective-c_tuesdays/')

        # section
        section = self.__tag(self.document.body, 'section')
        self.__tag(section, 'h1', text=self.title)
        section.extend(self.content)

        # section footer
        footer = self.__tag(section, 'footer')
        a = self.__tag(footer, 'a', href=self.entry.original_url)
        self.__tag(a, 'em', text=f'{self.entry.title}')
        footer.append(' was originally published on ')
        self.__tag(footer, 'time', text=self.published, datetime=self.published)
        footer.append('.')

    def find_links(self, links: Set[Tuple[str, str, str]], node: Optional[PageElement] = None):
        if not node:
            node = self.document
        if isinstance(node, Tag):
            if node.name == 'a':
                links.add(
                    (node['href'], self.entry.title, ' '.join(node.stripped_strings))
                )
            for child in node.children:
                self.find_links(links, child)

    def print_statistics(self, brief=True):
        print(self.entry.title)
        self.content.report.print_statistics(brief=brief)

    def __tag(
            self,
            parent: Tag,
            name: str,
            attrs: Optional[Dict[str, str]] = None,
            text: Optional[str] = None,
            **kwargs
    ) -> Tag:
        attrs = attrs if attrs else {}
        tag = self.document.new_tag(name, attrs=attrs, **kwargs)
        if text:
            tag.append(text)
        parent.append(tag)
        return tag

    def __extract_body_contents(self) -> List[PageElement]:
        contents = list(self.document.body.children)
        for node in contents:
            node.extract()
        return contents


def get_filename(entry: Entry) -> str:
    title = entry.title.lower()
    title = title.replace('objective-c tuesdays: ', '')
    title = title.replace('@', 'at-')
    title = title.replace('...', '-')
    title = title.replace(',', '')
    title = title.replace(' ', '_')
    return f'{title}.html'


def get_title(entry: Entry) -> str:
    title = entry.title.replace('Objective-C Tuesdays: ', '')
    title = title.title()
    title = title.replace('Nsarray', 'NSArray')
    return title
