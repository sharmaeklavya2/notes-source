#!/usr/bin/env python3

"""Create PDF files for all tex files in src/."""

import sys
import os
from os.path import join as pjoin
import argparse
import subprocess


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--no-clean', action='store_false', dest='clean', default=True,
    help="Do not remove temporary files from output directory")
parser.add_argument('--force', action='store_true', default=False,
    help="Build even if source was not updated")
parser.add_argument('--dryrun', action='store_true', default=False,
    help="Only print commands; do not run them")
ARGS = parser.parse_args(None if __name__ == '__main__' else [])


TRASH_EXTS = ['.aux', '.log', '.out', '.toc', '.bbl', '.blg']
BIBDB_PATH = 'bibdb.bib'
DRYRUN_PROMPT = '$ '


def is_source_updated(source, dest):
    source_mtime = os.path.getmtime(source)
    try:
        dest_mtime = os.path.getmtime(dest)
    except OSError:
        return True
    return dest_mtime <= source_mtime


def run(cmd, **kwargs):
    if ARGS.dryrun:
        print(DRYRUN_PROMPT + ' '.join(cmd))
    else:
        return subprocess.call(cmd, **kwargs)


def run_check(cmd, **kwargs):
    if ARGS.dryrun:
        print(DRYRUN_PROMPT + ' '.join(cmd))
    else:
        return subprocess.check_call(cmd, **kwargs)


def process_tex_file(ifpath, odpath):
    """Compile a tex file to a PDF.

    ifpath: Path to input file.
    odpath: Path to output directory.
    """

    name = os.path.splitext(os.path.basename(ifpath))[0]
    aux_path = pjoin(odpath, name + '.aux')
    pdf_path = pjoin(odpath, name + '.pdf')

    if not (ARGS.force or is_source_updated(ifpath, pdf_path)):
        print(' Skipped ' + ifpath)
    else:
        print('Building ' + ifpath)

        os.makedirs(odpath, exist_ok=True)
        pdflatex_args = ['pdflatex', '-interaction=batchmode', '-output-directory=' + odpath, ifpath]

        try:
            run_check(pdflatex_args, stdout=subprocess.DEVNULL)
            run(['bibtex', aux_path], stdout=subprocess.DEVNULL)
            run_check(pdflatex_args, stdout=subprocess.DEVNULL)
            run_check(pdflatex_args, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(e, file=sys.stderr)
            return False

    if ARGS.clean:
        for ext in TRASH_EXTS:
            fpath = pjoin(odpath, name + ext)
            if ARGS.dryrun:
                if os.path.exists(fpath):
                    print(DRYRUN_PROMPT + 'rm ' + fpath)
            try:
                os.remove(fpath)
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
