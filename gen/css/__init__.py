from functools import cache

from .css import CSS


@cache
def parse_css_file(path: str) -> CSS:
    return CSS(path)
