#!/usr/local/bin/python

import os
import sys
import yaml
import argparse
from pyvert import convert_dict


def main():

    parser = argparse.ArgumentParser(description='process a YAML file from'
                                                 ' a given directory path')
    parser.add_argument('--nohidden',
                        action='append_const',
                        dest='flags',
                        const='no-hidden',
                        default=[],
                        help='list only visible files and directories')
    parser.add_argument('-n', '--depth',
                        type=int,
                        action='store',
                        dest='max_depth',
                        default=0,
                        nargs='?',
                        help='max depth of subdirectory traversal.'
                             '0 (default) = full.')
    parser.add_argument('file',
                        help='path to YAML file to process')
    parser.add_argument('target',
                        nargs='?',
                        help='path of target directory (leave empty to use '
                             'current directory)')

    args = parser.parse_args()

    print args

    y = os.path.abspath(args.file)
    p = os.getcwd() if not args.target else os.path.abspath(args.target)

    if not os.path.exists(y):
        print("YAML file {} does not exist".format(y))
        sys.exit(1)

    if not os.path.exists(p):
        print("Path {} does not exist".format(p))
        sys.exit(1)

    try:
        with open(y, 'r') as f:
            try:
                d = yaml.load(f)
                print(d)
#               dest = process(data=d, path=p, args)
                print('Directory created at {}'.format(os.path.join(os.getcwd(), dest)))
                sys.exit(0)

            except Exception as e:
                print(e)
                sys.exit(1)

    except Exception as e:
        print(e)
        sys.exit(2)

def process(data, path, options):
    depth=0

    def process_inner(data, path=str()):
        """
        Return the top-level key of the passed dictionary

        Keyword arguments:
        data -- a dictionary with one top-level key
        path -- a system path as a string
        """

        depth += 1

        print depth

        if depth <= options.max_depth:
            dest = os.path.join(os.getcwd(), path)

            if isinstance(data, dict):
                for k, v in data.items():
                    os.makedirs(os.path.join(dest, k))
                    process_inner(v, os.path.join(path, str(k)))

            elif isinstance(data, list):
                for i in data:
                    if isinstance(i, dict):
                        process_inner(i, path)
                    else:
                        with open(os.path.join(dest, i), "a"):
                            os.utime(os.path.join(dest, i), None)

            if isinstance(data, dict):
                return list(data.keys())[0]


    process_inner(data, path)

if __name__ == '__main__':
    main()
