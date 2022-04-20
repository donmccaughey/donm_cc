from argparse import ArgumentParser, Namespace
from hyperlinks import check_external_links, http_external_links
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
    return arg_parser.parse_args()


def check_links(root):
    links = []
    root.accumulate_links(links)
    print(f'Found {len(links)} links')
    external_links = http_external_links(links)
    print(f'Checking {len(external_links)} external links')
    results = check_external_links(external_links)
    print(f'Found {len(results.broken_links)} broken links')
    for broken_link in results.broken_links:
        resource, href, status_code = broken_link
        print(f'  In {resource.path}: {href} returned {status_code}')
    print(f'Checked {len(external_links)} external links in {results.elapsed_seconds} seconds')


def main():
    options = get_options()

    root.find_files('../site-src')
    root.build_documents()

    if options.check_links:
        check_links(root)
    else:
        root.generate(
            '../wwwroot',
            is_dry_run=options.dry_run,
            overwrite=options.overwrite,
            omit_styles=options.omit_styles,
        )


if __name__ == '__main__':
    main()
