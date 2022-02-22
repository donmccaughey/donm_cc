import argparse
import os
import os.path
from atom import Feed


def get_args():
    arg_parser = argparse.ArgumentParser('Extract Objective-C Tuesdays')
    arg_parser.add_argument('xml_file', metavar='XML_FILE', type=str,
                            help='The Blogger XML dump to read')
    arg_parser.add_argument('output_dir', metavar='OUTPUT_DIR', type=str,
                            help='Location to write HTML files')
    return arg_parser.parse_args()


def main():
    args = get_args()
    if not os.path.exists(args.xml_file):
        print(f"The XML file {args.xml_file} doesn't exist")
        exit(1)
    feed = Feed(args.xml_file)
    feed.print_statistics(brief=True)

    os.makedirs(args.output_dir, exist_ok=True)
    for entry in feed.oc_tuesdays:
        entry.save(args.output_dir)


if __name__ == '__main__':
    main()
