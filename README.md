# organize

Real world data is messy:

1. the [IMF eLibrary Data](http://www.imf.org/external/data.htm) uses the ``.xls`` extension for TSV,
2. files on [data.gov](https://www.data.gov/) sometimes include preambles which break straightforward parsing,
3. if you've been using public data sources, then you have horror stories of your own.
4. (If all your data comes from coworkers or colleagues then undoubtedly it's always perfectly formatted.)

``organize`` aims to make it easy to eliminate the hand-scrub phase from working with real-world data files:

1. Read CSV, TSV and Excel formats, even if they are poorly labeled or missing a filename.
2. Skip over preambles lines which would otherwise require cleaning up by hand.
3. Ignore lines with whitespace or where every column is empty.

In most cases it should be as simple as:

    from organize import organize

    with open('myfile.csv|myfile.tsv|myfile.xls|myfile', 'r') as fin:
        for row in organize(fin):
            for column_name, column_value in row:
                print column_name, column_value

For best performance, also supply the filename or mimetype to help
prioritize the most likely parsers:

    for row in organize(fin, filename='myfile.csv', mimetype='text/csv'):
         # and so on

``organize`` owes a spiritual debt to [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/),
which similarly offered a sane abstraction over broken HTML, saving programmers great swaths of time
and energy.

Developed against Python 2.7, and hosted on [Github](https://github.com/lethain/organize).


## Installation

Simplest is to install via pip from [PyPi](https://pypi.python.org/pypi?name=organize):

    pip install organize

Alternative, you can install it from Github if you want an unreleased branch or commit:

    pip install -e git+https://github.com/lethain/organize#egg=organize

Note that installing from Github will also download the <5MB of test datasets
which are used when running the test suite. These are not installed when you
install the package via ``setup.py build install``.

For development:

    git clone git@github.com:lethain/organize.git
    cd organize
    make env

And then you can run the tests and stylechecks via:

    make test style


## Usage

For normal usage, ``organize`` presents a very simple interface:

    from organize import organize

    with open('myfile', 'r') as fin:
        for row in organize(fin):
            for name, val in row:
                print "%s: %s" % (name, val)

If possible, you should also pass the filename (or mimetype) to
the ``organize.organize`` function in order to prioritize the
parsers. Supplying the filename or mimetype will improve performance
in the normal case but will not impact correctness:

    from organize import organize

    filename = 'myfile.csv'
    mimetype = 'text/csv'
    with open('myfile', 'r') as fin:
        for row in organize(fin, filename=filename, mimetype=mimetype):
            for name, val in row:
                print "%s: %s" % (name, val)

In most cases there is no benefit to passing both filename and mimetype,
but for cases where you're reading a bunch of files, generally try to
supply as much information as possible.

Note that both the row and columns are generators, so you cannot
iterate through the returned generator multiple times. If you
wanted to process the same file twice, you would need to do
something like this:

    from organize import organize

    with open('myfile', 'r') as fin:
        for row in organize(fin):
            print row
        fin.seek(0)
        for row in organize(fin):
            print row


### Exposes duplicate columns, and unnamed columns

Because we don't want to accidentally drop data we do not
use a dictionary to store columns. This means by default you
will see all columns even if they are unnamed or have duplicate names.

If you do **not** want duplicates, you can convert the rows into dictionaries
simply by calling ``dict`` on each row:

    with open('myfile', 'r') as fin:
        for row in organize(fin):
            row_dict = dict(row)
            print row_dict.keys()

If you want uniqueness and ordering, then you can use [collections.OrderedDict](https://docs.python.org/2/library/collections.html#collections.OrderedDict):

    from collections import OrderedDict

    with open('myfile', 'r') as fin:
        for row in organize(fin):
            row_dict = OrderedDict(row)
            print row_dict.keys()


In this case you'll get the first value for each name.


### Only read certain rows

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


## Examples

This section briefly describes the contents of the ``examples`` directory.


### [transform_directory](organize/examples/transform_directory.py)

Walks through slurping up all files in a directory, organizing them,
and then writing the cleaned up versions into another directory.


### [Using with Pandas](organize/example/with_pandas.py)

[Pandas](http://pandas.pydata.org/) is one of the core Python
data science packages, and a commonly used tool. While it provides
many [tools for loading data](http://pandas.pydata.org/pandas-docs/stable/io.html),
it doesn't place as much emphasis on handling poorly formatted data.

    from organize import organize
    import pandas as pd

    pd.DataFrame.from_records(organize(open('myfile', 'r')))

The example file is a bit better formatted, but expresses the same idea.


## What it doesn't do

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


## Contribution and development

This section includes some commentary for those interested and willing to contribute
additions to this codebase. First, and most importantly: thank you!

Successful pull requests will pass pep8, pylint and tests, as well as including new
tests for any additional functionality (or fixed bugs). You can verify they are working
via:

    cd ~/path/to/organize
    make env test style

It's OK to disable certain pylint checks within the files you edit if it's not feasible
to resolve the pylint complaint. (For example, when it believes a given attribute doesn't
exist which does but it can't lint properly for whatever reason.)

### Areas for future development

We're using the [Github issue tracker](https://github.com/lethain/organize/issues) to
track specific projects for future development, but broadly there are two areas we'd
like to continue improving upon:

1. File parsing should be as robust as possible for existing formats.
2. File parsing should support as many formats as useful.

Anything along those lines that doesn't introduce significant complexity or
performance degradation will probably be viewed as a very good thing.


### Approach

Our implementation approach is:

1. The library should do the intended thing, even if it requires a hack
    or underwhelming heuristic.
2. Deal with streams, return streams. Many files are huge and we don't want
    to be needlessly wasteful.
3. Don't rely on filenames to identify data formats. Files are often mislabled or
    not labeled at all.

### Implemntation notes

This section includes a variety of implementation notes which may become somewhat relevant
to you in some odd edge-cases, but generally are not important for using the library.

#### Looking ahead a bit

We need to look ahead a bit at the beginning of files in order to exclude preamble
rows within a given dataset. This means that we will read some rows of the loaded
file before you explicitly load them.

From a user's point of view, this *should* be transparent as we will replay the rows
we've read in advance as if we're reading them when you read them. However, I would not
be shocked if in some rare and bizarre scenarios this leaks.