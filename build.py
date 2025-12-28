#!/usr/bin/env python3

"""Build all tex and markdown files in src to PDF and HTML respectively."""

import sys
import os
from os.path import join as pjoin
import argparse
import subprocess
import shlex


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('out_dir', help='Path to output directory')
parser.add_argument('--theme', choices=['dark', 'light', 'sepia'],
    help='Colorscheme to use for LaTeX documents')
parser.add_argument('--no-clean', action='store_false', dest='clean', default=True,
    help="Do not remove temporary files from output directory")
parser.add_argument('--force', action='store_true', default=False,
    help="Build even if source was not updated")
parser.add_argument('--dry-run', action='store_true', default=False,
    help="Only print commands; do not run them")
parser.add_argument('--no-date', dest='use_SDE_envvar', action='store_false', default=True,
    help='do not set the SOURCE_DATE_EPOCH envvar')
parser.add_argument('--verbose', action='store_true', default=False)
ARGS = parser.parse_args(None if __name__ == '__main__' else ['output'])


TRASH_EXTS = ['.aux', '.log', '.out', '.toc', '.bbl', '.blg']
BIBDB_PATH = 'bibdb.bib'
HTML_TEMPLATE_PATH = 'template.html'
CSS_PATH = 'style.css'
DRYRUN_PROMPT = '$ '


def is_source_updated(source, dest):
    source_mtime = os.path.getmtime(source)
    try:
        dest_mtime = os.path.getmtime(dest)
    except OSError:
        return True
    return dest_mtime <= source_mtime


def run(cmd, **kwargs):
    if ARGS.dry_run:
        print(DRYRUN_PROMPT + shlex.join(cmd))
    else:
        return subprocess.call(cmd, **kwargs)


def run_check(cmd, **kwargs):
    if ARGS.dry_run:
        print(DRYRUN_PROMPT + shlex.join(cmd))
    else:
        return subprocess.check_call(cmd, **kwargs)


global_markdown = None
global_html_template = None
global_css = None
global_dot_error = False
global_warn_count = 0

MD_EXT_CONFIGS = {
    'codehilite': {'guess_lang': False, 'use_pygments': True},
    'toc': {
        'title': 'Table of Contents',
        'toc_depth': "2-3",
    },
    'fenced_code': {},
    'md_in_html': {},
}


def get_markdown_and_template():
    global global_markdown
    if global_markdown is None:
        try:
            from markdown import Markdown
            global_markdown = Markdown(extensions=list(MD_EXT_CONFIGS.keys()), extension_configs=MD_EXT_CONFIGS)
        except ImportError as e:
            print('error while importing package markdown:', file=sys.stderr)
            print('{}: {}'.format(type(e).__name__, str(e)))
            print('WARNING: markdown files will not be processed')
            print('WARNING: make sure you have the Markdown python package (pip install Markdown)')
            global global_warn_count
            global_warn_count += 1
            global_markdown = False

    if global_markdown is False:
        markdown = None
    else:
        markdown = global_markdown

    global global_html_template
    if global_html_template is None:
        with open(HTML_TEMPLATE_PATH) as fp:
            global_html_template = fp.read()
    global global_css
    if global_css is None:
        with open(CSS_PATH) as fp:
            global_css = fp.read().strip()

    return (markdown, global_html_template, global_css)


def process_tex_file(ifpath, odpath):
    """Compile a tex file to a PDF.

    ifpath: Path to input file.
    odpath: Path to output directory.
    """

    name = os.path.splitext(os.path.basename(ifpath))[0]
    aux_path = pjoin(odpath, name + '.aux')
    pdf_path = pjoin(odpath, name + '.pdf')
    if ARGS.theme is None:
        main_arg = ifpath
    else:
        main_arg = '\\def\\colorscheme{' + ARGS.theme + '}\\input{' + ifpath + '}'

    if not (ARGS.force or is_source_updated(ifpath, pdf_path)):
        if ARGS.verbose:
            print(' Skipped ' + ifpath)
        status = 2
    else:
        print('Building ' + ifpath)

        os.makedirs(odpath, exist_ok=True)
        pdflatex_args = ['pdflatex', '-interaction=batchmode',
            '-output-directory=' + odpath, main_arg]

        try:
            run_check(pdflatex_args, stdout=subprocess.DEVNULL)
            run(['bibtex', aux_path], stdout=subprocess.DEVNULL)
            run_check(pdflatex_args, stdout=subprocess.DEVNULL)
            run_check(pdflatex_args, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(e, file=sys.stderr)
            return 0
        status = 1

    if ARGS.clean:
        for ext in TRASH_EXTS:
            fpath = pjoin(odpath, name + ext)
            if ARGS.dry_run:
                if os.path.exists(fpath):
                    print(DRYRUN_PROMPT + 'rm ' + fpath)
            else:
                try:
                    os.remove(fpath)
                except FileNotFoundError:
                    pass

    return status


def process_md_file(ifpath, odpath):
    """Compile a markdown file to HTML.

    ifpath: Path to input file.
    odpath: Path to output directory.
    """

    name = os.path.splitext(os.path.basename(ifpath))[0]
    html_path = pjoin(odpath, name + '.html')

    if not (ARGS.force or is_source_updated(ifpath, html_path)):
        if ARGS.verbose:
            print(' Skipped ' + ifpath)
        return 2
    else:
        print('Building ' + ifpath)
        os.makedirs(odpath, exist_ok=True)
        markdown, template, style = get_markdown_and_template()
        if markdown is not None and not ARGS.dry_run:
            with open(ifpath) as fp:
                input = fp.read()
            body = markdown.convert(input)
            output = template.format(style=style, body=body)
            with open(html_path, 'w') as fp:
                fp.write(output)
        return 1


def process_dot_file(ifpath, odpath):
    """Compile a dot file to SVG.

    ifpath: Path to input file.
    odpath: Path to output directory.
    """

    name = os.path.splitext(os.path.basename(ifpath))[0]
    svg_path = pjoin(odpath, name + '.svg')

    if not (ARGS.force or is_source_updated(ifpath, svg_path)):
        if ARGS.verbose:
            print(' Skipped ' + ifpath)
        return 2
    else:
        print('Building ' + ifpath)
        if ARGS.dry_run:
            print(DRYRUN_PROMPT + shlex.join(['mkdir', '-p', odpath]))
        else:
            os.makedirs(odpath, exist_ok=True)
        args = ['dot', '-Tsvg', ifpath, '-o', svg_path]
        try:
            run_check(args)
        except FileNotFoundError as e:
            global global_dot_error
            print('error while running dot:', file=sys.stderr)
            print(args, file=sys.stderr)
            print('{}: {}'.format(type(e).__name__, str(e)))
            if global_dot_error is False:
                global_dot_error = True
                global global_warn_count
                global_warn_count += 1
                print('WARNING: dot files will not be processed')
                print('WARNING: make sure you have dot (graphviz) installed')
    return 1


FUNC_BY_EXT = {
    '.tex': process_tex_file,
    '.md': process_md_file,
    '.dot': process_dot_file,
}


def process_by_ext(ifpath, odpath):
    ext = os.path.splitext(ifpath)[1]
    if ext in FUNC_BY_EXT:
        return FUNC_BY_EXT[ext](ifpath, odpath)
    else:
        if ARGS.verbose:
            print(' Ignoring ' + ifpath)
        return 3


def process_tree(ipath, opath, action, filter=None):
    """Recursively process files in a tree and output them in a new similarly-structured tree.

    ipath: Path to input directory or file.
    opath: Path to output directory or file.
    action: Function to call on each input file.
    filter: Function which decides whether to process a file/directory or not.

    Returns a tuple (n_failed, n_success, n_skipped)
    """

    status_agg = [0] * 4
    for entry in os.scandir(ipath):
        if filter is None or filter(entry):
            if entry.is_file():
                status = action(entry.path, opath)
                if status == 0:
                    print('{} failed'.format(entry.path), file=sys.stderr)
                status_agg[status] += 1
            elif entry.is_dir():
                status_agg2 = process_tree(pjoin(ipath, entry.name), pjoin(opath, entry.name),
                    action, filter)
                for i in range(len(status_agg)):
                    status_agg[i] += status_agg2[i]
            else:
                raise Exception('Encountered a strange file: ' + entry.path)
    return status_agg


def main():
    if ARGS.use_SDE_envvar:
        os.environ['SOURCE_DATE_EPOCH'] = '0'
    status_agg = process_tree('src', ARGS.out_dir, process_by_ext)
    if global_warn_count:
        print(global_warn_count, 'warnings')
    print('{} failed, {} built, {} skipped, {} ignored'.format(*status_agg))
    if status_agg[0]:
        sys.exit(2)


if __name__ == '__main__':
    main()
