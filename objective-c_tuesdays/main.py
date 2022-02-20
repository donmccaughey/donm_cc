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
    print(f'Found {len(feed.entries)} entries')
    print(f'Found {len(feed.posts)} posts')
    print()

    categories = set()
    for post in feed.posts:
        categories.update(post.categories)
    print(f'Found {len(categories)} categories:')
    for post in categories:
        print(f'  {post}')
    print()

    obj_c_titles = [
        post for post in feed.posts
        if (
                'objective' in post.title.lower()
                and 'objective-c_tuesdays' not in post.categories
        )
    ]
    print(f'Found {len(obj_c_titles)} posts with "Objective-C" in the title:')
    for post in obj_c_titles:
        print(f'  {post.title}')
    print()

    print(f'Found {len(feed.oc_tuesdays)} Objective-C Tuesdays posts:')
    os.makedirs(args.output_dir, exist_ok=True)
    for entry in feed.oc_tuesdays:
        print(f'  {entry.title}')
        print(f'      {entry.original_url}')
        print(f'      {entry.published}')
        entry.save(args.output_dir)
    print()


if __name__ == '__main__':
    main()
