import argparse

from hyperlinks import check_external_links
from website import root


def main():
    arg_parser = argparse.ArgumentParser('Generate the site')
    arg_parser.add_argument('--dry-run', action='store_true', default=False, help="don't write or copy files")
    arg_parser.add_argument('--overwrite', action='store_true', default=False, help='overwrite existing files')
    arg_parser.add_argument('--omit-styles', action='store_true', default=False, help='generate without stylesheet links')
    arg_parser.add_argument('--check-links', action='store_true', default=False, help='check that hyperlinks are valid')
    args = arg_parser.parse_args()

    root.find_files('../site-src')
    if args.check_links:
        links = []
        root.accumulate_links(links)
        print('Checking external links')
        results = check_external_links(links)
        print(f'Found {len(results.broken_links)} broken links')
        for broken_link in results.broken_links:
            resource, href, status_code = broken_link
            print(f'  In {resource.path}: {href} returned {status_code}')
        print(f'Scanned {len(results.external_links)} links in {results.elapsed_seconds} seconds')
    else:
        root.generate(
            '../wwwroot',
            is_dry_run=args.dry_run,
            overwrite=args.overwrite,
            omit_styles=args.omit_styles,
        )


if __name__ == '__main__':
    main()
