from xml.etree import ElementTree
from . import Entry, NAMESPACES


class Feed:
    def __init__(self, path):
        tree = ElementTree.parse(path)
        elements = tree.findall('atom:entry', NAMESPACES)
        self.entries = [Entry(element) for element in elements]
        self.posts = [entry for entry in self.entries if entry.kind == 'post']
        self.oc_tuesdays = [
            entry for entry in self.posts
            if 'objective-c_tuesdays' in entry.categories
        ]
