"""
Parse a variety of tabular data formats.

    >>> from organize import organize
    >>> for row in organize(open('myfile', 'r')):
            for col, val in row:
                print "%s: %s" % (col, val)

"""
from organize import parsers


class Organizer(object):
    """
    ``Organizer`` determines which formats to attempt to
    parse files with, and the order in which to parse them in.

    """
    def __init__(self, filename=None, mimetype=None, use_default_parsers=True, prepend_parsers=None, append_parsers=None, use_filename_hints=True, use_mimetype_hints=True):
        """
        Initialize Organizer.

        ``use_default_parsers`` is True or False, and if False does not load any standard parsers (CSV, etc),
            and you will only have the parsers you've listed in ``prepend_parsers`` and ``append_parsers``.
        ``prepend_parsers`` is a list of parser classes to try before default parsers
        ``append_parsers`` is a list of parser classes to try after default parsers
        ``use_filename_hints`` re-sorts the parsers to first try parsers that can use the specified filename or extension
        ``use_mimetype_hints`` re-sorts the parsers to first try parsers that can use the specified mimetype
        """
        prepend = prepend_parsers if prepend_parsers else []
        default = self.default_parsers() if use_default_parsers else []
        append = append_parsers if append_parsers else []
        parsers = prepend + default + append
        self.parsers = [parser() for parser in parsers]

    def default_parsers(self):
        "Find parsers for Organizer to support current formats."
        return parsers.registered_parsers()

    def determine_parser_order(self, filename=None, mimetype=None):
        "Determine order to attempt parsers."
        parser_order = []
        if filename:
            for parser in self.parsers:
                if parser.should_parse_by_filename(filename) and parser not in parser_order:
                    parser_order.append(parser)
        if mimetype:
            for parser in self.parsers:
                if parser.should_parse_by_mimetype(mimetype) and parser not in parser_order:
                    parser_order.append(parser)

        for parser in self.parsers:
            if parser not in parser_order:
                parser_order.append(parser)

        return parser_order

    def parse(self, stream, filename=None, mimetype=None):
        """
        Parse a file stream.

        ``stream`` is a file-like resource containing the data
        """
        parser_order = self.determine_parser_order(filename=filename, mimetype=mimetype)
        exception = None
        for parser in parser_order:
            stream.seek(0)
            try:
                if parser.can_parse(stream):
                    stream.seek(0)
                    return parser.parse(stream)
            except Exception, e:
                exception = e
        if exception:
            raise exception  # pylint: disable-msg=E0702


def organize(stream, filename=None, mimetype=None):
    """
    Read a file stream.

        >>> with open('mydata.csv', 'r') as fin:
                organize(fin)

    """
    return Organizer().parse(stream, filename=filename, mimetype=mimetype)
