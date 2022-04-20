from __future__ import annotations
import os
from typing import Optional

from hyperlinks import parse_links, only_internal_links, to_absolute_urls, only_page_links
from .directory import Directory
from .resource import Resource


class Sitemap(Resource):
    def __init__(
            self,
            root_url: str,
            parent: Optional[Directory] = None,
            **kwargs
    ):
        super().__init__(
            name='sitemap',
            parent=parent,
            **kwargs,
        )
        self.root_url = root_url

    def file_parts(self) -> list[str]:
        return ['sitemap.txt']

    def build_documents(self):
        pass

    def generate(
            self,
            output_path: str,
            is_dry_run=True,
            overwrite=False,
    ):
        links = []
        self.parent.accumulate_links(links)
        parsed_links = parse_links(links)
        internal_links = only_internal_links(parsed_links)
        page_links = only_page_links(internal_links)
        urls = set(to_absolute_urls(self.root_url, page_links))

        path = os.path.join(output_path, self.path)
        path = os.path.normpath(path)
        print('writing sitemap', path)
        if not is_dry_run:
            mode = 'w' if overwrite else 'x'
            with open(path, mode, encoding='utf8') as f:
                for url in sorted(urls):
                    f.write(f'{url}\n')
