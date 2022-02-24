import os
from atom import Entry
from bs4 import BeautifulSoup
from bs4.element import Doctype, Tag, PageElement
from typing import Dict, Optional, List

from page.content import Content


class Page:
    def __init__(self, entry: Entry, output_dir: str):
        self.content = None
        self.document = None
        self.entry = entry
        self.output_dir = output_dir

        self.filename = get_filename(self.entry)
        self.path = os.path.join(self.output_dir, self.filename)

    def __str__(self) -> str:
        return str(self.document)

    def build(self):
        self.document = BeautifulSoup(self.entry.content, 'html5lib')
        self.content = Content(self.document)

        self.document.insert(0, Doctype('html'))
        self.document.html['lang'] = 'en'

        # head
        self.__tag(self.document.head, 'meta', charset='utf-8')
        self.__tag(self.document.head, 'meta', attrs={
            'name': 'viewport',
            'content': 'initial-scale=0.9, width=device-width'
        })
        self.__tag(self.document.head, 'title', text=self.entry.title)
        self.__tag(self.document.head, 'link',
                   rel='stylesheet', href='/base.css')

        # body
        nav = self.__tag(self.document.body, 'nav')
        self.__tag(nav, 'a', text='Don McCaughey', href='/')
        nav.append(' • ')
        self.__tag(nav, 'a', text='Objective-C Tuesdays',
                   href='/objective-c_tuesdays/')

        section = self.__tag(self.document.body, 'section')
        self.__tag(section, 'h1', text=self.entry.title)

        section.extend(self.content)

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
    year = entry.published.year
    month = entry.published.month
    day = entry.published.day

    title = entry.title.lower()
    title = title.replace('objective-c tuesdays: ', '')
    title = title.replace('@', 'at-')
    title = title.replace('...', '-')
    title = title.replace(',', '')
    title = title.replace(' ', '_')
    return f'{year:04}-{month:02}-{day:02}-{title}.html'
