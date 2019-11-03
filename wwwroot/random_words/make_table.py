#!/usr/bin/env python

import os
import sys


input_file = 'word.list'
output_file = 'words.table'


def main():
    input_path = os.path.join(os.getcwd(), input_file)
    with file(input_path) as input:
        lines = input.readlines()
        words = [ word.strip() for word in lines ]

    max_length = 0
    for word in words: 
        length = len(word)
        if length > max_length:
            max_length = length 

    rows = [ word.ljust(max_length) + '\n' for word in words ]

    output_path = os.path.join(os.getcwd(), output_file)
    with file(output_path, 'w') as output:
        output.writelines(rows)

    row_count = len(words)
    row_width = max_length + 1
    file_size = row_count * row_width
    print('row count: {:d}'.format(row_count))
    print('row width: {:d}'.format(row_width))
    print('file size: {:,} bytes'.format(file_size))


if __name__ == '__main__':
  main()

