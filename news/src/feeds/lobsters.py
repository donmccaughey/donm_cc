from datetime import datetime

from news import Item, Source, URL
from .site import Site


class Lobsters(Site):
    def __init__(self, _options: dict):
        super().__init__(
            URL('https://lobste.rs/rss'),
            'Lobsters', 'lob',
        )

    def __repr__(self) -> str:
        return 'Lobsters()'

    def parse_entry(self, entry, now: datetime) -> Item:
        return Item(
            url=URL(entry.link),
            title=entry.title,
            source=Source(URL(entry.comments), self.initials),
            created=now,
            modified=now,
        )