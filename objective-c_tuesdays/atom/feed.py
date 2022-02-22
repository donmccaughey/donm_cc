from xml.etree import ElementTree
from . import Entry, NAMESPACES


class Feed:
    def __init__(self, path):
        tree = ElementTree.parse(path)
        elements = tree.findall('atom:entry', NAMESPACES)

        self.entries = [Entry(element) for element in elements]
        self.posts = [entry for entry in self.entries if entry.kind == 'post']

        self.categories = set()
        for post in self.posts:
            self.categories.update(post.categories)
        assert 'objective-c_tuesdays' in self.categories

        self.oc_titled_posts = [
            post for post in self.posts
            if (
                    'objective' in post.title.lower()
                    and 'objective-c_tuesdays' not in post.categories
            )
        ]

        self.oc_tuesdays = [
            entry for entry in self.posts
            if 'objective-c_tuesdays' in entry.categories
        ]

    def print_statistics(self, brief=True):
        print(f'Found {len(self.entries)} entries')
        print(f'Found {len(self.posts)} posts')
        print(f'Found {len(self.categories)} categories')
        if not brief:
            for category in sorted(self.categories):
                print(f'  {category}')
        print(f'Found {len(self.oc_titled_posts)} posts with "Objective-C" in the title')
        if not brief:
            for post in self.oc_titled_posts:
                print(f'  {post.title}')
        print(f'Found {len(self.oc_tuesdays)} Objective-C Tuesdays posts')
        if not brief:
            for post in self.oc_tuesdays:
                print(f'  {post.title}')
