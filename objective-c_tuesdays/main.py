import argparse
import os
import os.path
from typing import List

from atom import Feed
from page import FormattedPage, Page, Index


def main():
    args = get_args()
    if not os.path.exists(args.xml_file):
        print(f"The XML file {args.xml_file} doesn't exist")
        exit(1)
    feed = Feed(args.xml_file)
    feed.print_statistics(brief=args.brief)

    pages = [Page(entry, args.output_dir) for entry in feed.oc_tuesdays]
    set_topics(pages)

    url_map = {page.entry.original_url : page.new_url for page in pages}
    url_map |= URL_UPDATES

    print_links(pages, brief=args.brief)

    os.makedirs(args.output_dir, exist_ok=True)
    for page in pages:
        page.build(url_map)
        page.print_statistics(brief=args.brief)
        with open(page.path, 'w') as f:
            f.write(str(FormattedPage(page)))

    index = Index(pages)
    index.write(args.output_dir)


def get_args():
    arg_parser = argparse.ArgumentParser('Extract Objective-C Tuesdays')
    arg_parser.add_argument('--brief', action='store_true', default=False,
                            help='Show a brief report')
    arg_parser.add_argument('xml_file', metavar='XML_FILE', type=str,
                            help='The Blogger XML dump to read')
    arg_parser.add_argument('output_dir', metavar='OUTPUT_DIR', type=str,
                            help='Location to write HTML files')
    return arg_parser.parse_args()


def print_links(pages: List[Page], brief=False):
    links = set()
    for page in pages:
        page.find_links(links)
    if brief:
        urls = set([url for (url, title, text) in links])
        print(f'Found {len(urls)} unique links')
        for url in sorted(urls):
            print(f'    {url}')
    else:
        print(f'Found {len(links)} links')
        url_width = 0
        title_width = 0
        for (url, title, text) in sorted(links):
            url_width = max(len(url), url_width)
            title_width = max(len(title), title_width)
        for (url, title, text) in sorted(links):
            print(f'    {url:{url_width}} {title:{title_width}} {text}')


def set_topics(pages: List[Page]):
    for page in pages:
        page.topic, page.is_toc = TOPIC_MAP[page.entry.original_url]


TOPIC_MAP = {
    'http://blog.ablepear.com/2009/10/objective-c-tuesdays-for-loop.html': ('looping', False),
    'http://blog.ablepear.com/2009/10/objective-c-tuesdays-for-loop_13.html': ('looping', False),
    'http://blog.ablepear.com/2009/10/objective-c-tuesdays-forin-loop.html': ('looping', False),
    'http://blog.ablepear.com/2009/10/objective-c-tuesdays-while-loop.html': ('looping', False),
    'http://blog.ablepear.com/2009/11/objective-c-tuesdays-break-out-of-loop.html': ('looping', False),
    'http://blog.ablepear.com/2009/11/objective-c-tuesdays-continue.html': ('looping', False),
    'http://blog.ablepear.com/2009/11/objective-c-tuesdays-dowhile-loop.html': ('looping', False),
    'http://blog.ablepear.com/2009/12/objective-c-tuesdays-common-uses-for.html': ('looping', False),
    'http://blog.ablepear.com/2009/12/objective-c-tuesdays-global-variables.html': ('variables', False),
    'http://blog.ablepear.com/2009/12/objective-c-tuesdays-goto.html': ('looping', False),
    'http://blog.ablepear.com/2009/12/objective-c-tuesdays-looping-in.html': ('looping', True),
    'http://blog.ablepear.com/2010/01/objective-c-tuesdays-extern-and-global.html': ('variables', False),
    'http://blog.ablepear.com/2010/01/objective-c-tuesdays-static-variables.html': ('variables', False),
    'http://blog.ablepear.com/2010/03/objective-c-tuesdays-static-variables.html': ('variables', False),
    'http://blog.ablepear.com/2010/04/objective-c-tuesdays-instance-variables.html': ('variables', False),
    'http://blog.ablepear.com/2010/04/objective-c-tuesdays-instance-variables_20.html': ('variables', False),
    'http://blog.ablepear.com/2010/04/objective-c-tuesdays-local-variables.html': ('variables', False),
    'http://blog.ablepear.com/2010/04/objective-c-tuesdays-property-and.html': ('variables', False),
    'http://blog.ablepear.com/2010/05/objective-c-tuesdays-atomic-and.html': ('variables', False),
    'http://blog.ablepear.com/2010/05/objective-c-tuesdays-changing-default.html': ('variables', False),
    'http://blog.ablepear.com/2010/05/objective-c-tuesdays-synthesizing.html': ('variables', False),
    'http://blog.ablepear.com/2010/06/objective-c-tuesdays-c-strings.html': ('strings', False),
    'http://blog.ablepear.com/2010/06/objective-c-tuesdays-variables-in.html': ('variables', True),
    'http://blog.ablepear.com/2010/06/objective-c-tuesdays-writing-thread.html': ('variables', False),
    'http://blog.ablepear.com/2010/07/objective-c-tuesdays-string-literals.html': ('strings', False),
    'http://blog.ablepear.com/2010/07/objective-c-tuesdays-unicode-string.html': ('strings', False),
    'http://blog.ablepear.com/2010/07/objective-c-tuesdays-wide-character.html': ('strings', False),
    'http://blog.ablepear.com/2010/08/objective-c-tuesdays-concatenating.html': ('strings', False),
    'http://blog.ablepear.com/2010/09/objective-c-tuesdays-searching-in.html': ('strings', False),
    'http://blog.ablepear.com/2010/09/objective-c-tuesdays-slicing-and-dicing.html': ('strings', False),
    'http://blog.ablepear.com/2010/09/objective-c-tuesdays-string-comparison.html': ('strings', False),
    'http://blog.ablepear.com/2010/10/objective-c-tuesdays-replacing-in.html': ('strings', False),
    'http://blog.ablepear.com/2011/07/objective-c-tuesdays-arrays.html': ('data structures', False),
    'http://blog.ablepear.com/2011/07/objective-c-tuesdays-dynamic-arrays.html': ('data structures', False),
    'http://blog.ablepear.com/2011/07/objective-c-tuesdays-regular.html': ('strings', False),
    'http://blog.ablepear.com/2011/07/objective-c-tuesdays-strings-in.html': ('strings', True),
    'http://blog.ablepear.com/2011/08/objective-c-tuesdays-more-about-dynamic.html': ('data structures', False),
    'http://blog.ablepear.com/2011/11/objective-c-tuesdays-sorting-arrays.html': ('data structures', False),
    'http://blog.ablepear.com/2011/12/objective-c-tuesdays-more-nsarray.html': ('data structures', False),
}

URL_UPDATES = {
    'http://developer.apple.com/IPhone/library/documentation/Cocoa/Reference/Foundation/Classes/NSArray_Class/NSArray.html':
        'https://developer.apple.com/documentation/foundation/nsarray?language=objc',

    'http://developer.apple.com/IPhone/library/documentation/Cocoa/Reference/Foundation/Classes/NSEnumerator_Class/Reference/Reference.html#//apple_ref/doc/c_ref/NSEnumerator':
        'https://developer.apple.com/documentation/foundation/nsenumerator?language=objc',

    'http://developer.apple.com/iPhone/library/documentation/Cocoa/Reference/Foundation/Classes/NSDictionary_Class/Reference/Reference.html':
        'https://developer.apple.com/documentation/foundation/nsdictionary?language=objc',

    'http://developer.apple.com/iPhone/library/documentation/Cocoa/Reference/Foundation/Classes/NSSet_Class/Reference/Reference.html':
        'https://developer.apple.com/documentation/foundation/nsset?language=objc',

    'http://developer.apple.com/iphone/library/documentation/Cocoa/Conceptual/Multithreading/Introduction/Introduction.html#//apple_ref/doc/uid/10000057i-CH1-SW1':
        'https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Multithreading/Introduction/Introduction.html',

    'http://developer.apple.com/iphone/library/documentation/system/conceptual/manpages_iphoneos/man3/iconv.3.html':
        'https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/iconv.3.html',

    'http://developer.apple.com/library/ios/#DOCUMENTATION/System/Conceptual/ManPages_iPhoneOS/man3/qsort.3.html':
        'https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/qsort.3.html',

    'http://developer.apple.com/library/ios/#documentation/System/Conceptual/ManPages_iPhoneOS/man3/regex.3.html':
        'https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/regex.3.html',

    'http://developer.apple.com/library/ios/#documentation/cocoa/conceptual/KeyValueCoding/Articles/KeyValueCoding.html':
        'https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueCoding/index.html',

    'http://en.wikipedia.org/wiki/Basic_Multilingual_Plane#Basic_Multilingual_Plane':
        'https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane',

    'http://en.wikipedia.org/wiki/Buffer_overflow':
        'https://en.wikipedia.org/wiki/Buffer_overflow',

    'http://en.wikipedia.org/wiki/C99':
        'https://en.wikipedia.org/wiki/C99',

    "http://en.wikipedia.org/wiki/Don't_repeat_yourself":
        "https://en.wikipedia.org/wiki/Don't_repeat_yourself",

    'http://en.wikipedia.org/wiki/ISO/IEC_8859-7':
        'https://en.wikipedia.org/wiki/ISO/IEC_8859-7',

    'http://en.wikipedia.org/wiki/POSIX':
        'https://en.wikipedia.org/wiki/POSIX',

    'http://en.wikipedia.org/wiki/Quicksort':
        'https://en.wikipedia.org/wiki/Quicksort',

    'http://en.wikipedia.org/wiki/The_C_Programming_Language_(book)':
        'https://en.wikipedia.org/wiki/The_C_Programming_Language',

    'http://en.wikipedia.org/wiki/UTF-16/UCS-2#Encoding_of_characters_outside_the_BMP':
        'https://en.wikipedia.org/wiki/UTF-16#Code_points_from_U+010000_to_U+10FFFF',

    'http://en.wikipedia.org/wiki/Unicode_normalization':
        'https://en.wikipedia.org/wiki/Unicode_equivalence#Normalization',

    'http://en.wiktionary.org/wiki/cromulent':
        'https://en.wiktionary.org/wiki/cromulent',

    'http://futurama.wikia.com/wiki/Good_news,_everyone!':
        'https://futurama.fandom.com/wiki/Good_news,_everyone!',

    'http://oreilly.com/catalog/9780596520694/':
        'https://www.oreilly.com/library/view/regular-expressions-cookbook/9780596802837/',

    'http://oreilly.com/catalog/9780596528126/':
        'https://www.oreilly.com/library/view/mastering-regular-expressions/0596528124/',

    'http://pubs.opengroup.org/onlinepubs/009695399/basedefs/xbd_chap09.html':
        'https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap09.html',

    'http://site.icu-project.org/': 'https://icu.unicode.org',

    'http://source.icu-project.org/repos/icu/icu/trunk/license.html':
        'https://github.com/unicode-org/icu/blob/main/icu4c/LICENSE',

    'http://unicode.org/faq/normalization.html':
        'https://unicode.org/faq/normalization.html',

    'http://www.aarp.org/':
        'https://www.aarp.org',

    'http://www.pcre.org/':
        'https://www.pcre.org',

    'http://www.pragprog.com/articles/tell-dont-ask':
        'https://web.archive.org/web/20200426154726/https://pragprog.com/articles/tell-dont-ask',
}


if __name__ == '__main__':
    main()
