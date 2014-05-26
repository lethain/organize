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
    """
    mimetypes = ('application/vnd.ms-excel')
    extensions = ('.xls', '.excel', '.xlsx', '.xlsm', '.xltm', '.xltx', '.xlsb')

    def can_parse(self, stream):
        "Can parse this as an Excel file."

    def get_worksheet(self, workbook):
        """
        Pick the best worksheet from workbook.
        
        Later should consider using longest one rather
        than simple the first one.
        """
        for worksheet_name in workbook.sheet_names():
            return workbook.sheet_by_name(worksheet_name)

    def parse(self, stream):
        "Parse this file as Excel file."
        # right , so the sad truth is that xlrd
        # does not play very well with data streams
        # and wants to be able to reread the same data
        # multiple times, so we will just have to oblige
        # then, as painful as that happens to be
        contents = stream.read()

        workbook = xlrd.open_workbook(file_contents=contents)
        worksheet = self.get_worksheet(workbook)
        print "worksheet", worksheet

