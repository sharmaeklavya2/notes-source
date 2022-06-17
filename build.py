#!/usr/bin/env python3

"""Build all tex and markdown files in src to PDF and HTML respectively."""

import sys
import os
from os.path import join as pjoin
import argparse
import subprocess


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('out_dir', help='Path to output directory')
parser.add_argument('--no-clean', action='store_false', dest='clean', default=True,
    help="Do not remove temporary files from output directory")
parser.add_argument('--force', action='store_true', default=False,
    help="Build even if source was not updated")
parser.add_argument('--dry-run', action='store_true', default=False,
    help="Only print commands; do not run them")
parser.add_argument('--no-date', dest='use_SDE_envvar', action='store_false', default=True,
    help='do not set the SOURCE_DATE_EPOCH envvar')
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
        print(DRYRUN_PROMPT + ' '.join(cmd))
    else:
        return subprocess.call(cmd, **kwargs)


def run_check(cmd, **kwargs):
    if ARGS.dry_run:
        print(DRYRUN_PROMPT + ' '.join(cmd))
    else:
        return subprocess.check_call(cmd, **kwargs)


global_markdown = None
global_html_template = None
global_css = None
global_dot_error = False
global_warn_count = 0


def get_markdown_and_template():
    global global_markdown
    if global_markdown is None:
        try:
            from markdown import Markdown
            global_markdown = Markdown(extensions=['fenced_code'])
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

    if not (ARGS.force or is_source_updated(ifpath, pdf_path)):
        print(' Skipped ' + ifpath)
    else:
        print('Building ' + ifpath)

        os.makedirs(odpath, exist_ok=True)
        pdflatex_args = ['pdflatex', '-interaction=batchmode',
            '-output-directory=' + odpath, ifpath]

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
            if ARGS.dry_run:
                if os.path.exists(fpath):
                    print(DRYRUN_PROMPT + 'rm ' + fpath)
            else:
                try:
                    os.remove(fpath)
                except FileNotFoundError:
                    pass

    return True


def process_md_file(ifpath, odpath):
    """Compile a markdown file to HTML.

    ifpath: Path to input file.
    odpath: Path to output directory.
    """

    name = os.path.splitext(os.path.basename(ifpath))[0]
    html_path = pjoin(odpath, name + '.html')

    if not (ARGS.force or is_source_updated(ifpath, html_path)):
        print(' Skipped ' + ifpath)
    else:
        print('Building ' + ifpath)
        os.makedirs(odpath, exist_ok=True)
        markdown, template, style = get_markdown_and_template()
        if markdown is not None:
            with open(ifpath) as fp:
                input = fp.read()
            body = markdown.convert(input)
            output = template.format(style=style, body=body)
            with open(html_path, 'w') as fp:
                fp.write(output)

    return True


def process_dot_file(ifpath, odpath):
    """Compile a dot file to SVG.

    ifpath: Path to input file.
    odpath: Path to output directory.
    """

    name = os.path.splitext(os.path.basename(ifpath))[0]
    svg_path = pjoin(odpath, name + '.svg')

    if not (ARGS.force or is_source_updated(ifpath, svg_path)):
        print(' Skipped ' + ifpath)
    else:
        print('Building ' + ifpath)
        os.makedirs(odpath, exist_ok=True)
        args = ['dot', '-Tsvg', ifpath, '-o', svg_path]
        try:
            subprocess.check_call(args)
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

    return True


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
    if ARGS.use_SDE_envvar:
        os.environ['SOURCE_DATE_EPOCH'] = '0'
    success = process_tree('src', ARGS.out_dir, process_by_ext)
    if global_warn_count:
        print(global_warn_count, 'warnings')
    if not success:
        sys.exit(2)


if __name__ == '__main__':
    main()
