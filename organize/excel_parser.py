"Parser for Excel files."
"Comma Separated Values Parser."
from cStringIO import StringIO
from itertools import islice, chain, izip_longest
import xlrd
from organize.parsers import Parser


class ExcelParser(Parser):
    """
    A parser which handles Excel.

    Excel is pretty expressive, so we're basically just
    cherry-picking the first worksheet. This is clearly
    not a great long-term strategy.

    Right , so the sad truth is that xlrd does not play
    very well with data streams and wants to be able to
    reread the same data multiple times, so we will just
    have to oblige then, as painful as that happens to be
    """
    mimetypes = ('application/vnd.ms-excel', 'application/vs-excel')
    extensions = ('.xls', '.excel', '.xlsx', '.xlsm', '.xltm', '.xltx', '.xlsb')

    def file_contents(self, stream):
        """
        Return file contents for workbook.

        Ideally we'd do some kind of lazy stream reading
        which caches after it's read. This would allow us
        to avoid reading everything if we don't need it
        while also not requiring xlrd to know how to use
        streams properly.
        """
        return stream.read()

    def can_parse(self, stream):
        "Can parse this as an Excel file."
        try:
            xlrd.open_workbook(file_contents=self.file_contents(stream))
            return True
        except:
            return False

    def get_worksheet(self, workbook):
        """
        Pick the best worksheet from workbook.

        Later should consider using longest one rather
        than simple the first one.
        """
        for worksheet_name in workbook.sheet_names():
            return workbook.sheet_by_name(worksheet_name)

    def rows(self, sheet):
        "Filter out preamble from rows."

        num_cols_per_line = []
        start = 0
        previous = None
        for row_index in range(sheet.nrows):
            row = sheet.row_values(row_index)

            # this is probably a bit weak to simply use the
            # non-empty columns, perhaps a more robust check
            # would be to use the last empty column, although
            # in some situations that would likely not work either
            num_cols = len([x for x in row if x])
            if num_cols > 0:
                num_cols_per_line.append(num_cols)
                if previous is not None:
                    if num_cols > previous * 2:
                        start = row_index
                previous = num_cols

        headers = sheet.row_values(start)
        for row_index in range(start+1, sheet.nrows):
            cols = sheet.row_values(row_index)
            if len([x for x in cols if x]):
                yield izip_longest(headers, cols)

    def parse(self, stream):
        "Parse this file as Excel file."
        book = xlrd.open_workbook(file_contents=self.file_contents(stream))
        sheet = self.get_worksheet(book)
        return self.rows(sheet)
