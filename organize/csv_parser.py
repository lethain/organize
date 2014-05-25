"CSV Parser."
import csv
from itertools import islice, chain, izip_longest
from organize.parsers import Parser


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
    lines_to_test = 25

    def without_blank_lines(self, stream):
        "Filter out blank lines."
        to_strip = '\t\r\n %s' % self.delimiter
        for line in stream:
            if line.strip(to_strip):
                yield line

    def guess_dialect(self, txt):
        "Try to guess CSV dialect."
        utf8_txt = txt.encode('utf-8')
        return csv.Sniffer().sniff(utf8_txt, delimiters=self.delimiter)

    def can_parse(self, stream):
        "Can parse this file as CSV."
        lines = islice(self.without_blank_lines(stream), self.lines_to_test)
        txt = '\n'.join(lines)
        try:
            dialect = self.guess_dialect(txt)
            if self.delimiter in txt:
                return True
            return False
        except csv.Error:
            return False       

    def parse(self, stream):
        """
        Parse this file as CSV.
        """
        lines = self.without_blank_lines(stream)
        lines_for_dialect = list(islice(lines, self.lines_to_test))
        dialect = self.guess_dialect('\n'.join(lines_for_dialect))

        # we need to chain the lines we read for dialect detection together
        # with the rest of the unread lines to avoid rereading or dropping
        # their contents
        reader = unicode_csv_reader(chain(lines_for_dialect, lines), dialect=dialect)

        # use first row for headers
        headers = list(islice(reader, 0, 1))[0]

        for row in reader:
            yield ((name,val) for name, val in izip_longest(headers, row))

