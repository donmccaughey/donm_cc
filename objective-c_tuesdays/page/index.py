import os.path
from typing import List, TextIO

from page import Page


class Index:
    def __init__(self, pages: List[Page]):
        self.pages = pages
        self.topics = ['looping', 'variables', 'strings', 'data structures']

    def write(self, output_dir: str):
        path = os.path.join(output_dir, 'index.page')
        with open(path, 'w') as f:
            f.write(HEADER)
            for topic in self.topics:
                write_topic(f, topic, self.pages)


def write_topic(f: TextIO, topic: str, pages: List[Page]):
    f.write('\n')
    f.write('\n')
    f.write(f'.section links {topic.title()}\n')
    tocs = [page for page in pages if page.is_toc and page.topic == topic]
    for toc in sorted(tocs, key=lambda page: page.published):
        write_link(f, toc)
    regulars = [page for page in pages if not page.is_toc and page.topic == topic]
    for regular in sorted(regulars, key=lambda page: page.published):
        write_link(f, regular)


def write_link(f: TextIO, page: Page):
    f.write('\n')
    f.write(f'.link blog {page.title}\n')
    f.write(f'.url {page.new_url}\n')
    f.write(f'.date {page.published}\n')


HEADER = '''.page links Objective-C Tuesdays

When the [iPhone SDK](https://en.wikipedia.org/wiki/IOS_SDK#History) was 
released in 2008, my good friend [Kevin](https://bomberry.com) and I formed 
Able Pear Software, a small consultancy focused on mobile development.  From
2009 through 2011, I wrote a series of posts for our 
[company blog](http://blog.ablepear.com) called _Objective-C Tuesdays_ 
(published on Tuesdays, naturally).

We weren't the only people drawn to iPhone development, but outside of a small 
cadre of Mac programmers, Objective-C was largely unknown.  It's also very 
different from most mainstream programming languages, being a Smalltalk-inspired
dynamic layer atop the venerable C language -- with very unusual syntax.  There
was very little learning material available at the time, either for purchase or
free on the Internet, and Apple's terse documentation left big gaps to fill.

So I did my part to help.  I focused on the basics: loops, variables, strings 
and arrays, and wrote about both the dynamic, high level
[Foundation classes](https://developer.apple.com/documentation/foundation?language=objc)
and the low level, static C equivalents.
'''
