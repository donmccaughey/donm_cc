from atom import Entry
from bs4 import BeautifulSoup
from bs4.element import Doctype


class Page:
    def __init__(self, entry: Entry):
        self.entry = entry

        self.document = BeautifulSoup(self.entry.content, 'html5lib')
        self.filename = get_filename(self.entry)

    def cleanup(self):
        doctype = Doctype('html')
        self.document.insert(0, doctype)
        self.document.html['lang'] = 'en'
        self.build_head()

    def build_head(self):
        charset = self.document.new_tag('meta')
        charset['charset'] = 'utf-8'
        self.document.head.append(charset)


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
