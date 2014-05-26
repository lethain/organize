"Test Excel parsing."
import organize.excel_parser
from itertools import islice
from organize.tests import OrganizeTestCase


class TestExcelParser(OrganizeTestCase):
    "Test Excel."
    def setUp(self):
        "Test Excel parser."
        self.parser = organize.excel_parser.ExcelParser()
        self.first_line = [
            (u'Year', 1901),
            (u'Increase', 1),
            (u'Decrease', 14),
            (u'Grade', u'A'),
        ]

    def test_should_parse_by_mimetype(self):
        "Responds to proper mimetype."
        self.assertTrue(self.parser.should_parse_by_mimetype('application/vs-excel'))
        self.assertTrue(self.parser.should_parse_by_mimetype('application/vnd.ms-excel'))
        self.assertFalse(self.parser.should_parse_by_mimetype('text/csv'))
        self.assertFalse(self.parser.should_parse_by_mimetype('text/tsv'))

    def test_should_parse_by_filename(self):
        "Responds to proper extensions."
        self.assertTrue(self.parser.should_parse_by_filename('myfile/test.xls'))
        self.assertTrue(self.parser.should_parse_by_filename('myfile/test.xlsx'))
        self.assertFalse(self.parser.should_parse_by_filename('myfile/test.csv'))
        self.assertFalse(self.parser.should_parse_by_filename('myfile/test.tsv'))

    def test_can_parse(self):
        "Test determining which files are parsable."
        for filename in self.excel_filenames:
            with self.file_handle(filename) as fh:
                self.assertTrue(self.parser.can_parse(fh))

        for filename in self.tsv_filenames + self.csv_filenames:
            with self.file_handle(filename) as fh:
                self.assertFalse(self.parser.can_parse(fh))

    def test_parse_xlsx(self):
        "Test parsing Excel files."
        filename = 'excel/simple.xlsx'
        with self.file_handle(filename) as fh:
            first = list(self.parser.parse(fh).next())
            self.assertEquals(first, self.first_line)

    def test_parse_xls(self):
        "Test parsing Excel-97 files."
        filename = 'excel/simple_old.xls'
        with self.file_handle(filename) as fh:
            first = list(self.parser.parse(fh).next())
            self.assertEquals(first, self.first_line)

    def test_parse_skip_whitespace(self):
        "Test parsing Excel files."
        filename = 'excel/simple_whitespace.xlsx'
        with self.file_handle(filename) as fh:
            first = list(self.parser.parse(fh).next())
            self.assertEquals(first, self.first_line)

    def test_parse_with_preamble(self):
        "Test parsing a file with a preamble."
        filename = "excel/irrat_exu_robert_shiller.xlsx"
        num_rows = 0
        with self.file_handle(filename) as fh:
            for row in self.parser.parse(fh):
                row_lst = list(row)
                self.assertTrue(len(row_lst) >= 10, row_lst)
                num_rows += 1
        self.assertTrue(num_rows > 1500)
