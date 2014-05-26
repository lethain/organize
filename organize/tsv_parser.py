"Tab Separated Values parser."
import csv
import string
from organize.csv_parser import CSVParser
from itertools import islice


class TSVParser(CSVParser):
    """
    A parser which handles TSV data.

    A very lightweight subclass of ``CSVParser``.
    """
    mimetypes = ('text/tsv')
    extensions = ('.tsv')
    delimiter = '\t'
    default_dialect = csv.excel_tab

    def guess_dialect(self, txt):
        "CSV sniffer does not work well for TSV."
        return None

    def can_parse(self, stream):
        "Can parse this file as TSV."
        try:
            lines = islice(self.without_preamble(self.without_blank_lines(stream)), self.lines_to_test)
            for line in lines:
                if not string.count(line, self.delimiter):
                    return False
            return True
        except:
            return False
