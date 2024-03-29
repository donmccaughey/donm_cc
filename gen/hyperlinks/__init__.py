from __future__ import annotations
from typing import TYPE_CHECKING

import requests
import sys
import time

from dataclasses import dataclass
from pathlib import PurePosixPath
from urllib.parse import ParseResult, urlparse, urljoin

if TYPE_CHECKING:
    from resources.resource import Resource


BAD_HOSTS = ['www.linkedin.com']
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15'


@dataclass
class LinkCheckResults:
    broken_links: list[(Resource, str, int)]
    elapsed_seconds: int


def check_link(session: requests.Session, href: str) -> int:
    try:
        response = session.head(href, headers={'User-Agent': USER_AGENT}, timeout=5)
        status_code = response.status_code
    except OSError:
        status_code = 0
    if 200 == status_code:
        return 200

    try:
        response = session.get(href, headers={'User-Agent': USER_AGENT}, stream=True, timeout=5)
        for _ in response.iter_content(chunk_size=None):
            pass
        status_code = response.status_code
    except OSError:
        status_code = 0
    return status_code


def check_external_links(external_links: list[(Resource, str, ParseResult)]) -> LinkCheckResults:
    links = sorted(external_links, key=lambda link: link[1])

    session = requests.Session()
    start_time = time.monotonic()

    broken_links = []
    count = 0
    line_width = 75
    sys.stdout.write(f' 0% ')
    for link in links:
        resource, href, url = link
        status_code = check_link(session, href)
        if 200 == status_code:
            sys.stdout.write('.')
            sys.stdout.flush()
        else:
            if url.netloc in BAD_HOSTS:
                sys.stdout.write('*')
            else:
                sys.stdout.write('x')
            sys.stdout.flush()
            broken_links.append((resource, href, status_code))
        count += 1
        if 0 == count % line_width:
            percent = int(count / len(links) * 100)
            sys.stdout.write('\n')
            sys.stdout.write(f'{percent:2}% ')
            sys.stdout.flush()
    sys.stdout.write('\n')

    stop_time = time.monotonic()
    elapsed_seconds = int(stop_time - start_time)

    return LinkCheckResults(
        broken_links=broken_links,
        elapsed_seconds=elapsed_seconds,
    )


def http_external_links(links: list[(Resource, str)]) -> list[(Resource, str, ParseResult)]:
    parsed_links = parse_links(links)
    external_links = only_external_links(parsed_links)
    return only_http_links(external_links)


def parse_links(links: list[(Resource, str)]) -> list[(Resource, str, ParseResult)]:
    parsed_links = []
    for link in links:
        resource, href = link
        url = urlparse(href)
        parsed_links.append((resource, href, url))
    return parsed_links


def is_internal_link(link: (Resource, str, ParseResult)) -> bool:
    parse_result = link[2]
    return not parse_result.scheme and not parse_result.netloc


def only_internal_links(links: list[(Resource, str, ParseResult)]) -> list[(Resource, str, ParseResult)]:
    return [link for link in links if is_internal_link(link)]


def only_external_links(links: list[(Resource, str, ParseResult)]) -> list[(Resource, str, ParseResult)]:
    return [link for link in links if link[2].netloc]


def only_http_links(links: list[(Resource, str, ParseResult)]) -> list[(Resource, str, ParseResult)]:
    return [link for link in links if ('http' == link[2].scheme or 'https' == link[2].scheme)]


def only_page_links(links: list[(Resource, str, ParseResult)]) -> list[(Resource, str, ParseResult)]:
    page_links = []
    for link in links:
        resource, url, parse_result = link
        if parse_result.path:
            path = PurePosixPath(parse_result.path)
            if not path.suffix or path.suffix in ['.html', '.md', '.pdf', '.txt']:
                page_links.append(link)
    return page_links


def to_absolute_urls(root_url: str, links: list[(Resource, str, ParseResult)]) -> list[str]:
    return [urljoin(root_url, link[1]) for link in links]
