from __future__ import annotations

import dataclasses
import sys
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

import requests

from urllib.parse import quote_plus

from file_formats.page_file import BookLink
from resources import PageFile


@dataclass
class OpenLibraryDocs:
    key: str
    type: str
    title: str
    json: Dict[str, Any]


@dataclass
class OpenLibraryResults:
    book_link: BookLink
    search_url: str
    error: Optional[str]
    docs: list[OpenLibraryDocs]


def find_book_links(page_files: List[PageFile]) -> List[BookLink]:
    links = []
    for page_file in page_files:
        default_author = None
        if 'author' == page_file.page_file.modifier:
            default_author = page_file.page_file.title
        for section in page_file.page_file.sections:
            for link in section.links:
                if isinstance(link, BookLink):
                    if default_author and default_author not in link.authors:
                        copy = dataclasses.replace(link)
                        copy.authors = list(link.authors) + [default_author]
                        link = copy
                    links.append(link)
    return links


def open_library_search_url(book_link: BookLink) -> str:
    parameters = [
        f'title={quote_plus(book_link.title)}'
    ] + [
        f'author={quote_plus(author)}' for author in book_link.authors
    ]
    query = '&'.join(parameters)
    return 'http://openlibrary.org/search.json?' + query


def search_open_library(book_link: BookLink) -> OpenLibraryResults:
    search_url = open_library_search_url(book_link)
    try:
        response = requests.get(search_url)
    except OSError as e:
        error = f'ERROR: {e}'
        return OpenLibraryResults(
            book_link=book_link, search_url=search_url, error=error, docs=list()
        )
    if 200 != response.status_code:
        error = f'ERROR: {response.status_code} {response.reason}'
        return OpenLibraryResults(
            book_link=book_link, search_url=search_url, error=error, docs=list()
        )
    json = response.json()
    docs = []
    if 'docs' in json:
        for doc in json['docs']:
            key = doc['key'] if 'key' in doc else '(no key)'
            type = doc['type'] if 'type' in doc else '(no type)'
            title = doc['title'] if 'title' in doc else '(no title)'
            docs.append(OpenLibraryDocs(key, type, title, doc))
    return OpenLibraryResults(
        book_link=book_link, search_url=search_url, error=None, docs=docs
    )
