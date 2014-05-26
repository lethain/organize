"Sanitize a directory of files into CSV."
import argparse
from itertools import islice
from os import listdir
from os.path import isfile, join, split, splitext
from organize import organize
import csv


def list_filepaths(path):
    "List all files in a directory."
    exts = ('.csv', '.tsv', '.xls', '.excel', '.xlsx', '.xlsm', '.xltm', '.xltx', '.xlsb')
    for filename in listdir(path):
        filepath = join(path, filename)
        if isfile(filepath):
            _, ext = splitext(filepath)
            if ext in exts:
                yield filepath


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transform data files in directory into CSV.')
    parser.add_argument('src_dir', metavar='src_dir', help='path to transform')
    parser.add_argument('dest_dir', metavar='dest_dir', help='path to transform')
    args = parser.parse_args()

    for filepath in list_filepaths(args.src_dir):
        _, filename = split(filepath)
        with open(filepath, 'r') as fin:
            rows = organize(fin, filename=filename)
            dest = join(args.dest_dir, filename)
            print "Writing %s to %s" % (filepath, dest)
            with open(dest, 'w') as fout:
                writer = csv.writer(fout)
                first = list(islice(rows, 1))
                if len(first):
                    first = list(first[0])

                    # write header row based on first row
                    writer.writerow([x[0] for x in first])
                    # write value row based on first row
                    writer.writerow([x[1] for x in first])

                    # for remaining rows just write the data
                    for row in rows:
                        writer.writerow([x[1] for x in row])
