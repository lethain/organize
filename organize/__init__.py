"""
Parse a variety of tabular data formats.

    >>> from optimize import optimize
    >>> for row in optimize(open('myfile', 'r')):
            for col, val in row:
                print "%s: %s" % (col, val)

"""
from organize import parsers


class Optimizer(object):
    """
    ``Optimizer`` determines which formats to attempt to
    parse files with, and the order in which to parse them in.

    """
    default_formats = ['csv', 'tsv', 'excel']

    def __init__(self, stream, filename=None, mimetype=None, use_default_parsers=True, prepend_parsers=None, append_parsers=None, use_filename_hints=True, use_mimetype_hints=True):
        """
        Initialize Optimizer.

        ``stream`` is a file-like resource containing the data
        ``formats`` optional, is a list of formats to check
        ``use_default_parsers`` is True or False, and if False does not load any standard parsers (CSV, etc),
            and you will only have the parsers you've listed in ``prepend_parsers`` and ``append_parsers``.
        ``prepend_parsers`` is a list of parser classes to try before default parsers
        ``append_parsers`` is a list of parser classes to try after default parsers
        ``use_filename_hints`` re-sorts the parsers to first try parsers that can use the specified filename or extension
        ``use_mimetype_hints`` re-sorts the parsers to first try parsers that can use the specified mimetype
        """
        self.stream = stream
        prepend = prepend_parsers if prepend_parsers else []
        default = self.default_parsers() if use_default_parsers else []
        append = append_parsers if append_parsers else []
        self.parsers = prepend + default + append

    def default_parsers(self):
        "Find parsers for Optimizer to support current formats."
        return parsers.registered_parsers()


def optimize(stream, formats=None):
    """
    Read a file stream.

        >>> with open('mydata.csv', 'r') as fin:
                optimize(fin)

    ``formats`` takes a list of strings representing file formats.

    You can select the support formats and also the
    order in which to try determining the formats.
    """
    pass
