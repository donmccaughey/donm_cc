from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

import requests

from urllib.parse import quote_plus

from file_formats.page_file import BookLink


@dataclass
class OpenLibraryDocs:
    key: str
    type: str
    title: str
    json: Dict[str, Any]


@dataclass
class OpenLibraryResults:
    docs: list[OpenLibraryDocs]


def open_library_search_url(book_link: BookLink) -> str:
    parameters = [
        f'title={quote_plus(book_link.title)}'
    ] + [
        f'author={quote_plus(author)}' for author in book_link.authors
    ]
    query = '&'.join(parameters)
    return 'http://openlibrary.org/search.json?' + query


def search_open_library(url: str) -> OpenLibraryResults | Exception | int:
    try:
        response = requests.get(url)
    except OSError as e:
        return e
    if 200 != response.status_code:
        return response.status_code
    json = response.json()
    docs = []
    if 'docs' in json:
        for doc in json['docs']:
            key = doc['key'] if 'key' in doc else '(no key)'
            type = doc['type'] if 'type' in doc else '(no type)'
            title = doc['title'] if 'title' in doc else '(no title)'
            docs.append(OpenLibraryDocs(key, type, title, doc))
    return OpenLibraryResults(docs)
