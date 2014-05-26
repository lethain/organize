"Comma Separated Values Parser."
import csv
from itertools import islice, chain, izip_longest
from organize.parsers import Parser
from cStringIO import StringIO


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    """
    csv.py doesn't do Unicode; encode temporarily as UTF-8

    See: https://docs.python.org/2.7/library/csv.html
    """
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data), dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    """
    Work around for csv module's utf-8 issues.

    See: https://docs.python.org/2.7/library/csv.html
    """
    for line in unicode_csv_data:
        yield line.encode('utf-8')


class CSVParser(Parser):
    """
    A parser which handles CSV. This is a bit different than
    the Python CSV module which is really a *SV module in disguise.

    As such, this CSVParser is intentionally more restrictive to
    try to address situations where a file is valid CSV and valid
    TSV at the same time (but one of them is coherent and the other
    is largely incoherent).

    ``organize.tsv.TSVParser`` lightly subclasses this class.
    """
    mimetypes = ('text/csv')
    extensions = ('.csv')
    delimiter = ','
    default_dialect = csv.excel
    lines_to_test = 25

    def guess_dialect(self, txt):
        "Try to guess CSV dialect."
        utf8_txt = txt.encode('utf-8')
        try:
            return csv.Sniffer().sniff(utf8_txt, delimiters=self.delimiter)
        except:
            pass

    def can_parse(self, stream):
        "Can parse this file as CSV."
        try:
            lines = islice(self.without_preamble(self.without_blank_lines(stream)), self.lines_to_test)
            txt = '\n'.join(lines)
            dialect = self.guess_dialect(txt)
            if dialect and self.delimiter in txt:
                return True
            return False
        except:
            return False

    def without_preamble(self, stream):
        """
        Remove a stream's preamble if any.

        This is necessarily pretty hacky. What we do here is parse
        the first few lines for columns until we stabilize on a given
        number of rows. If early rows have a different number of columns
        then we cut them off.
        """
        lines = list(islice(stream, self.lines_to_test))
        num_cols_per_line = []
        start = 0
        previous = None
        for i, line in enumerate(lines):
            num_cols = len(list(csv.reader(StringIO(line), delimiter=self.delimiter))[0])
            num_cols_per_line.append(num_cols)
            if previous is not None:
                if num_cols > previous * 2:
                    start = i
            previous = num_cols

        for line in chain(lines[start:], stream):
            yield line

    def parse(self, stream):
        """
        Parse this file as CSV.
        """
        lines = self.without_preamble(self.without_blank_lines(stream))
        lines_for_dialect = list(islice(lines, self.lines_to_test))
        dialect = self.guess_dialect('\n'.join(lines_for_dialect))
        if not dialect:
            dialect = self.default_dialect

        # we need to chain the lines we read for dialect detection together
        # with the rest of the unread lines to avoid rereading or dropping
        # their contents
        reader = unicode_csv_reader(chain(lines_for_dialect, lines), dialect=dialect)

        # use first row for headers
        headers = list(islice(reader, 0, 1))[0]

        for row in reader:
            yield ((name, val) for name, val in izip_longest(headers, row))
