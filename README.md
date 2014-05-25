# organize

Data is messy in the real world. The [IMF eLibrary Data](http://www.imf.org/external/data.htm) uses the
``.xls`` extension for their TSV files, many files on [data.gov](https://www.data.gov/) include preambles
which break straightforward parsing, and these are hardly the darkest crimes of storing tabular data.

``organize`` aims to make it easy to eliminate the hand-scrub phase from working with real-world data files.
In most cases it should be as simple as:

    from organize import organize

    with open('myfile.csv|myfile.tsv|myfile.xls|myfile', 'r') as fin:
        for row in organize(fin):
            for column_name, column_value in row:
                print column_name, column_value

It owes a spiritual debt to [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/), which
similarly offered a sane abstraction over broken HTML, saving programmers great swaths of time and
energy.

Developed against Python 2.7, and hosted on [Github](https://github.com/lethain/organize).


## Approach

Our implementation approach is:

1. The library should do the intended thing, even if it requires a hack
    or underwhelming heuristic.
2. Deal with streams, return streams.


## What It Does Not Do

``organize`` tries to parse tabular data files, and any tabular data file it does
not parse is a bug. However, there are many things it does not do.
These are not necessarily the final say, but represent our best current thinking.


### Does not read directly from databases

We do not plan to support reading directly from databases (MySQL, PostgreSQL, SQLite, MongoDB, ...).


### Does not generate or enforce schemas

We do not intend to create or enforce schemas on the organized data itself.
Data will always be what the underlying format parser returns. For TSV, CSV,
Excel this means a string, for more helpful formats like JSON it will be a
string or integer or whatnot.

We like this functionality, but believe it would be best suited to
a different library built on top of ``organize`` as opposed to including
it directly within the library itself.


## Installation

For development

    git clone git@github.com:lethain/organize.git
    cd organize
    virtualenv env
    . ./env/bin/activate
    pip install -r requirements.txt
    python setup.py develop

And then you can run the tests via

    python tests/tests.py


## Usage

For normal usage, ``organize`` tries to present a very simple interface:

    from organize import organize

    with open('myfile', 'r') as fin:
        for row in organize(fin):
            for name, val in row:
                print "%s: %s" % (name, val)

Note that both read the rows and reading the columns within the rows are
dealing with generators to avoid reading the entire file into memory if you
only want a few rows. If you wanted to process the same file twice, you
would need to do something like this:

    with open('myfile', 'r') as fin:
        for row in organize(fin):
            print row
        fin.seek(0)
        for row in organize(fin):
            print row

Otherwise, it should really be that simple!

### Usage with Pandas

[pandas](http://pandas.pydata.org/)

*to be written*

### Duplicate columns, unnamed columns

Because we don't want to accidentally drop data we do not
use a dictionary to store columns. This means by default you
will see all columns even if they are unnamed or have duplicate names.

If you do **not** want duplicates, you can get ordered dictionaries
of the rows instead:

    with open('myfile', 'r') as fin:
        for row in organize(fin):
            for name, val in row.dict():
                print name, val

In this case you'll get the first value for each name.

### Only Using Certain Columns

Sometimes you might want to restrict the columns retrieved when you're iterating
through the dataset. You can do that via:

    with open('myfile', 'r') as fin:
        for row in organize(fin):
            for name, val in row.columns('name', 'age', 'gender'):
                print name, val

This is also the syntax for ensuring that a column is returned even if a given
row does not happen to have it, with a value of ``None`` (if the row does have the
value but it is empty, then it will be an empty string, ``""``, rather than ``None``,
``None`` is only possible in formats which can explicitly not include a column like
JSON, and will not occur for formats like CSV or TSV which have no such mechanism).


### Only Read Certain Rows

For some reason you may only want a subset of rows.
For getting a subset of rows we recommend using [itertools.islice](https://docs.python.org/2/library/itertools.html#itertools.islice)
from the Python ``itertools`` module:

    with open('myfile', 'r') as fin:
        for row in islice(organize(fin), 5, 25):
            print row

Note that you won't get the literal rows 5 through 25 from the document,
but rather rows 5 through 25 from the dataset extracted from the document.
I honestly have no idea why you'd actually want to do this. If you do have
a usecase, please let us know.

## Contribution and Development

This section includes some commentary for those interested and willing to contribute
additions to this codebase. First, and most importantly: thank you!

There are three guidelines for successful merging of pull requests:

1. Please make them pep8 compliant. We don't necessarily love pep8, but it's easier
    to work with a shared standard.
2. Please make sure pylint passes.
3. Please make sure the unit tests pass and that you add additional unit tests for
    new functionality.


### Running Pep8, Pylint and Tests

We do run with all of pep8, but we also acknowledge pylint can be a bit of a pain.
You are generally welcome to disable certain pylint checks within the files you edit
if it's not feasible to resolve the pylint complaint. (For example, when it believes
a given attribute doesn't exist which does but it can't lint properly for whatever reason.)

All tests should pass.

You can run these via:

    python tests/tests.py
    pep8 organize
    pylint organize

So help us all.

### Implemntation Notes

This section includes a variety of implementation notes which may become somewhat relevant
to you in some odd edge-cases, but generally are not important for using the library.

#### Looking Ahead A Bit

We need to look ahead a bit at the beginning of files in order to exclude preamble
rows within a given dataset. This means that we will read some rows of the loaded
file before you explicitly load them.

From a user's point of view, this *should* be transparent as we will replay the rows
we've read in advance as if we're reading them when you read them. However, I would not
be shocked if in some rare and bizarre scenarios this leaks.