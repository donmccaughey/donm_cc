from feedparser import FeedParserDict, parse

from .daring_fireball import DaringFireball


def test_keep_entry_keeps_essay():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <link rel="alternate" type="text/html" href="https://daringfireball.net/2022/11/twitter_tumult" />
            <title>★ Twitter Tumult</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert df.keep_entry(entry)


def test_keep_entry_keeps_linked():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <link rel="alternate" type="text/html" href="https://www.forbes.com/sites/emilybaker-white/2022/12/22/tiktok-tracks-forbes-journalists-bytedance/" />
            <link rel="related" type="text/html" href="https://daringfireball.net/linked/2022/12/22/tiktok-forbes-spying" />
            <title>TikTok Spied on Forbes Journalists</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert df.keep_entry(entry)


def test_keep_entry_rejects_linked_sponsor():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <link rel="alternate" type="text/html" href="https://workos.com/?utm_source=daringfireball&amp;utm_medium=newsletter&amp;utm_campaign=df2023"/>
            <link rel="related" type="text/html" href="https://daringfireball.net/linked/2023/02/12/workos"/>
            <title>WorkOS</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert not df.keep_entry(entry)


def test_keep_entry_rejects_no_title():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <link rel="alternate" type="text/html" href="https://www.forbes.com/sites/emilybaker-white/2022/12/22/tiktok-tracks-forbes-journalists-bytedance/" />
            <link rel="related" type="text/html" href="https://daringfireball.net/linked/2022/12/22/tiktok-forbes-spying" />
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert not df.keep_entry(entry)


def test_keep_entry_rejects_no_links():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <title>TikTok Spied on Forbes Journalists</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert not df.keep_entry(entry)


def test_keep_entry_rejects_sponsors_link():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <link rel="alternate" type="text/html" href="https://retool.com/?utm_source=sponsor&amp;utm_medium=newsletter&amp;utm_campaign=daringfireball" />
            <link rel="related" type="text/html" href="https://daringfireball.net/feeds/sponsors/2022/12/retool_5" />
            <title>[Sponsor] Retool</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert not df.keep_entry(entry)


def test_keep_entry_rejects_the_talk_show_link():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <link rel="alternate" type="text/html" href="https://daringfireball.net/thetalkshow/2022/12/22/ep-365" />
            <link rel="related" type="text/html" href="https://daringfireball.net/linked/2022/12/22/the-talk-show-365" />
            <title>The Talk Show: ‘Permanent September’</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert not df.keep_entry(entry)


def test_keep_entry_rejects_dithering_link():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <link rel="alternate" type="text/html" href="https://dithering.fm/"/>
            <link rel="related" type="text/html" href="https://daringfireball.net/linked/2023/02/03/dithering"/>
            <title>Dithering</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert not df.keep_entry(entry)