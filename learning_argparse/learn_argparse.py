#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import sys
import argparse


"""
Learning Argparse
"""

REPORT_TAGS = ['pass', 'fail', 'error']    

def dir_arg(arg):
    if os.path.isdir(arg):
        return arg
    else:
        msg = '%s is not a directory' %arg
        raise argparse.ArgumentTypeError(msg)

def main():
    print 'hello'



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Inspects and report on the Python test cases.',
        prog='testimony')
    parser.add_argument(
        'report', type=str, choices=REPORT_TAGS,
        metavar='REPORT',
        help='report type, possible values: %s' % ', '.join(REPORT_TAGS))
    parser.add_argument(
        'paths', metavar='PATH', type=dir_arg, nargs='+',
        help='a list of paths to look for tests cases')
    parser.add_argument(
        '-n', '--nocolor', action='store_true', help='Do not use color option')

    args = parser.parse_args() 
    main()