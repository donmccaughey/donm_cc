from __future__ import annotations
from typing import TYPE_CHECKING

import requests
import sys
import time

from dataclasses import dataclass
from urllib.parse import ParseResult, urlparse

if TYPE_CHECKING:
    from resources.resource import Resource


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15'


@dataclass
class LinkCheckResults:
    broken_links: list[(Resource, str, int)]
    elapsed_seconds: int


def check_external_links(external_links: list[(Resource, str, ParseResult)]) -> LinkCheckResults:
    start_time = time.monotonic()

    broken_links = []
    count = 0
    line_width = 75
    sys.stdout.write(f' 0% ')
    for link in external_links:
        resource, href, url = link
        response = requests.get(href, headers={'User-Agent': USER_AGENT})
        if 200 == response.status_code:
            sys.stdout.write('.')
            sys.stdout.flush()
        else:
            sys.stdout.write('x')
            sys.stdout.flush()
            broken_links.append((resource, href, response.status_code))
        count += 1
        if 0 == count % line_width:
            percent = int(count / len(external_links) * 100)
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


def only_external_links(links: list[(Resource, str, ParseResult)]) -> list[(Resource, str, ParseResult)]:
    return [link for link in links if link[2].netloc]


def only_http_links(links: list[(Resource, str, ParseResult)]) -> list[(Resource, str, ParseResult)]:
    return [link for link in links if ('http' == link[2].scheme or 'https' == link[2].scheme)]
