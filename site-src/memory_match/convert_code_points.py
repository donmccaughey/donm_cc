#!/usr/bin/env python

import argparse
import os.path
import re
import sys


def get_options():
    parser = argparse.ArgumentParser(description='Convert Unicode code points to JavaScript strings.')
    parser.add_argument('--input', dest='input_path', action='store',
            help='JavaScript file to read')
    parser.add_argument('--output', dest='output_path', action='store',
            help='JavaScript file to write')
    parser.add_argument('codepoints', metavar='CODEPOINT', type=str, nargs='*',
            help='Hexadecimal codepoints to convert')
    return parser.parse_args()


def convert_codepoint(codepoint_string):
    """
    See https://en.wikipedia.org/wiki/UTF-16 for conversion algorithm.
    """
    codepoint_hex = codepoint_string[2:] if codepoint_string.lower().startswith('u+') else codepoint_string
    codepoint = int(codepoint_hex, 16)
    twenty_bits = codepoint - 0x010000
    high_ten_bits = twenty_bits >> 10
    high_surrogate = high_ten_bits + 0xd800
    low_ten_bits = twenty_bits & 0x3ff
    low_surrogate = low_ten_bits + 0xdc00
    return '\\u%X\\u%X' % (high_surrogate, low_surrogate)


def convert_js_file(input_path, output_path):
    pattern = r"""\s+ \[' \\u \{ ([0-9a-f]{5}) \}', '([^']+)' \], """
    pattern = r"""\s+ \[' \\u \{ ([0-9a-f]{5}) \}', \s* '([^']*)' \], """
    regex = re.compile(pattern, re.IGNORECASE | re.VERBOSE)
    input = file(input_path, 'r')
    output = file(output_path, 'w') if output_path else sys.stdout
    for line in input:
        match = regex.match(line)
        if match:
            codepoint = match.group(1)
            name = match.group(2)
            js_string = convert_codepoint(codepoint)
            output.write("    ['%s', '%s'], // '\\u{%s}'\n" % (js_string, name, codepoint))
        else:
            output.write(line)
    output.close()
    input.close()


def main():
    options = get_options()

    if options.input_path:
        convert_js_file(options.input_path, options.output_path)

    for codepoint in options.codepoints:
        js_string = convert_codepoint(codepoint)
        print('%s = %s' % (codepoint, js_string))


if __name__ == '__main__':
    main()

