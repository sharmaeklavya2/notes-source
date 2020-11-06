# Notes

This repository contains notes I wrote while studying computer science.

Currently all notes are written in LaTeX and markdown.

To compile all latex files to PDF and all markdown files to HTML at once, run

    python3 build.py output

This requires python 3.5+ and `pdflatex` to be installed.
This will put all generated PDF and HTML files in a directory named `output`.

Alternatively, you can access the PDF and HTML files at <https://sharmaeklavya2.github.io/notes/>.

## auto-index

If you want the output directory to be navigable from a web browser,
get [`auto-index.py`](https://github.com/sharmaeklavya2/auto-index) and run

    python3 auto-index.py output

## How to report build failures

If the build process fails for you, feel free to
[report a bug](https://github.com/sharmaeklavya2/notes/issues/new) on GitHub.
In the bug report, please mention the file(s) whose build failed, the error message and your operating system.

When a LaTeX build fails, the error message will include the failed `pdflatex` command.
For example:

    Building src/cmo/01-preliminaries.tex
    Command '['pdflatex', '-interaction=batchmode', '-output-directory=output/cmo', 'src/cmo/01-preliminaries.tex']' returned non-zero exit status 1.
    src/cmo/01-preliminaries.tex failed

When this happens, run the `pdflatex` command without the `-interaction=batchmode` flag, i.e.:

    pdflatex -output-directory=output/cmo src/cmo/01-preliminaries.tex

This will make `pdflatex` produce more output detailing the cause of the failure.
Please also include this extra output in your bug report if possible.
