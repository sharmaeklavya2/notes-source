#!/usr/bin/env python3

"""Create PDF files for all tex files in src/."""

import sys
import os
from os.path import join as pjoin
import argparse
import subprocess


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--verbose', action='store_true', default=False)
parser.add_argument('--clean', action='store_true', default=False,
    help="Remove temporary files from output directory")
ARGS = parser.parse_args(None if __name__ == '__main__' else [])


TRASH_EXTS = ['.aux', '.log', '.out', '.toc']


def process_tex_file(ifpath, odpath):
    """Compile a tex file to a PDF.

    ifpath: Path to input file.
    odpath: Path to output directory.
    """

    if ARGS.verbose:
        print('process_tex_file({}, {})'.format(repr(ifpath), repr(odpath)))

    os.makedirs(odpath, exist_ok=True)
    for i in range(2):
        retcode = subprocess.call(['pdflatex', '-interaction=batchmode',
            '-output-directory=' + odpath, ifpath], stdout=subprocess.DEVNULL)
        if retcode != 0:
            return False

    if ARGS.clean:
        name = os.path.splitext(os.path.basename(ifpath))[0]
        for ext in TRASH_EXTS:
            try:
                os.remove(pjoin(odpath, name + ext))
            except FileNotFoundError:
                pass

    return True


def process_tree(ipath, opath, action, filter=None):
    """Recursively process files in a tree and output them in a new similarly-structured tree.

    ipath: Path to input directory or file.
    opath: Path to output directory or file.
    action: Function to call on each input file.
    filter: Function which decides whether to process a file/directory or not.
    """

    success = True
    for entry in os.scandir(ipath):
        if filter is None or filter(entry):
            if entry.is_file():
                success2 = action(entry.path, opath)
                if not success2:
                    success = False
                    print('{} failed'.format(entry.path), file=sys.stderr)
            elif entry.is_dir():
                process_tree(pjoin(ipath, entry.name), pjoin(opath, entry.name), action, filter)
            else:
                raise Exception('Encountered a strange file: ' + entry.path)
    return success


def main():
    success = process_tree('src', 'output', process_tex_file,
        (lambda entry: entry.is_dir() or os.path.splitext(entry.name)[1] == '.tex'))
    if not success:
        sys.exit(2)


if __name__ == '__main__':
    main()
