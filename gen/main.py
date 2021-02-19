import argparse
from website import root


def main():
    arg_parser = argparse.ArgumentParser('Generate the site')
    arg_parser.add_argument('--dry-run', action='store_true', default=False, help="don't write or copy files")
    arg_parser.add_argument('--overwrite', action='store_true', default=False, help='overwrite existing files')
    arg_parser.add_argument('--omit-styles', action='store_true', default=False, help='generate without stylesheet links')
    args = arg_parser.parse_args()

    root.find_files('../site-src')
    root.generate(
        '../wwwroot',
        is_dry_run=args.dry_run,
        overwrite=args.overwrite,
        omit_styles=args.omit_styles,
    )


if __name__ == '__main__':
    main()
