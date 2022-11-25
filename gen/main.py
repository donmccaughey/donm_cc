import dataclasses
import sys
from argparse import ArgumentParser, Namespace

from books import open_library_search_url, search_open_library, OpenLibraryResults, find_book_links
from file_formats.page_file import BookLink
from hyperlinks import check_external_links, http_external_links
from resources import Directory, Page, PageFile
from website import root


def get_options() -> Namespace:
    arg_parser = ArgumentParser('Generate the site')
    arg_parser.add_argument('--dry-run', action='store_true', default=False,
                            help="don't write or copy files")
    arg_parser.add_argument('--overwrite', action='store_true', default=False,
                            help='overwrite existing files')
    arg_parser.add_argument('--omit-styles', action='store_true', default=False,
                            help='generate without stylesheet links')
    arg_parser.add_argument('--check-links', action='store_true', default=False,
                            help='check that hyperlinks are valid')
    arg_parser.add_argument('--find-books', action='store_true', default=False,
                            help='search for books in Open Library')
    options = arg_parser.parse_args()
    options.source_dir = '../site-src'
    options.output_dir = '../wwwroot'
    return options


def check_links(root: Directory) -> int:
    links = root.find_all_links()
    print(f'Found {len(links)} links')
    external_links = http_external_links(links)
    print(f'Checking {len(external_links)} external links')
    results = check_external_links(external_links)
    print(f'Found {len(results.broken_links)} broken links')
    for broken_link in results.broken_links:
        resource, href, status_code = broken_link
        print(f'  In {resource.path}: {href} returned {status_code}')
    print(f'Checked {len(external_links)} external links in {results.elapsed_seconds} seconds')
    return len(results.broken_links)


def find_books(root: Directory):
    page_files = [resource for resource in root.all if isinstance(resource, PageFile)]
    book_links = find_book_links(page_files)
    print(f'Found {len(book_links)} book links')
    search_results = [
        search_open_library(book_link) for book_link in book_links
    ]
    error_results = [
        search_result for search_result in search_results if search_result.error
    ]
    good_results = [
        search_result for search_result in search_results if not search_result.error
    ]

    no_results = [
        search_result for search_result in good_results if not search_result.docs
    ]
    one_result = [
        search_result for search_result in good_results if 1 == len(search_result.docs)
    ]
    multiple_results = [
        search_result for search_result in good_results if len(search_result.docs) > 1
    ]

    if no_results:
        print(f'No search results for {len(no_results)} books:')
        for search_result in sorted(no_results, key=lambda r: r.book_link.title):
            print(f'    - "{search_result.book_link.title}"')

    if multiple_results:
        print(f'Multiple search results for {len(multiple_results)} books:')
        for search_result in sorted(multiple_results, key=lambda r: r.book_link.title):
            print(f'    - "{search_result.book_link.title}"')
            count = len(search_result.docs)
            if count > 10:
                print(f'        - Found {count} matches')
            else:
                for doc in search_result.docs:
                    print(f'        - [{doc.type}] "{doc.title}" https://openlibrary.org{doc.key}')

    if one_result:
        print(f'One search result for {len(one_result)} books:')
        for search_result in sorted(one_result, key=lambda r: r.book_link.title):
            doc = search_result.docs[0]
            print(f'    - [{doc.type}] "{doc.title}" https://openlibrary.org{doc.key}')

    if error_results:
        print(f'Search errors for {len(error_results)} books:')
        for search_result in sorted(error_results, key=lambda r: r.book_link.title):
            print(f'    - "{search_result.book_link.title}" - {search_result.error}')


def omit_styles(root: Directory):
    for resource in root:
        if isinstance(resource, Page):
            page: Page = resource
            page.remove_stylesheets()


def merge_stylesheets(root: Directory, source_dir: str):
    for resource in root:
        if isinstance(resource, Page):
            page: Page = resource
            page.merge_stylesheets(source_dir)


def main():
    options = get_options()

    root.find_files(options.source_dir)
    root.build_documents()

    if options.check_links:
        broken_count = check_links(root)
        sys.exit(broken_count)

    if options.find_books:
        find_books(root)
        sys.exit(0)

    if options.omit_styles:
        omit_styles(root)
    else:
        merge_stylesheets(root, options.source_dir)

    root.generate(
        options.output_dir,
        is_dry_run=options.dry_run,
        overwrite=options.overwrite,
    )


if __name__ == '__main__':
    main()
