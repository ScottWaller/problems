#!/usr/bin/env python

import argparse
import functools
from collections import namedtuple

FILTER_SYNTAX_HELP = "Filter Syntax: [include,exclude] data_type data_value \nMultiple Filter Syntax: filter1, filter2. Ex: include ip 1.1.1.1, exclude os Windows, ..."
DATA_TYPES = ('os', 'browser', 'ip', 'timestamp', 'filename', 'referer', 'line')
logline = namedtuple('logiline', " ".join(DATA_TYPES))

def parse_filter_args(filter_string):
    filters = filter_string.split(',')

def generate_filter(filter_string):
    parse_filter_args(filter_string)
    pass

def generate_logline(line):
    words = line.split()
    import ipdb; ipdb.set_trace()
    ip = words[0]


    return logiline(os, browser, ip, timestamp, filename, referer, line)

def parse_args():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='''
    ./filter_log.py --logfile <filename> --mode [loop,single] --filters (use filter syntax)
    {}'''.format(FILTER_SYNTAX_HELP), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--logfile", required=True, help="Logfile to do filtering on")
    parser.add_argument("--mode", choices=('loop', 'single'), default='single', help='Choose mode. Loop will ask you for filters repeatedly, Single will only do one set of filters and return after printing.')
    parser.add_argument("--filters", nargs='*', help='Use filter syntax to input include/exclude filters for the logfile')
    return parser.parse_args()

def main():
    args = parse_args()

    logfile = open(args.logfile)

    loglines = [generate_logline(logfile.readline())]

    for line in loglines:
        if _filter(line):
            print line



if __name__ == "__main__":
    main()