"Test TSV parsing."
from itertools import islice
import organize.tsv_parser
from organize.tests import OrganizeTestCase


class TestTSVParser(OrganizeTestCase):
    "Test TSV."
    def setUp(self):
        "Test TSV parser."
        self.parser = organize.tsv_parser.TSVParser()
        self.first_line = [
            (u'Year', u'2014'),
            (u'GRA Disbursements', u'2,765,465,000'),
            (u'GRA Repurchases', u'5,427,052,823'),
            (u'GRA Charges Paid', u'584,358,716'),
            (u'PRGT Disbursements', u'63,266,571'),
            (u'PRGT Repayments', u'132,553,847'),
            (u'PRGT Interest Paid', u'0'),
            (u'Total Disbursements', u'2,828,731,571'),
            (u'Total Repayments', u'5,559,606,670'),
            (u'Total Charges and Interest', u'584,358,716'),
        ]

    def test_should_parse_by_mimetype(self):
        "Responds to proper mimetype."
        self.assertTrue(self.parser.should_parse_by_mimetype('text/tsv'))
        self.assertFalse(self.parser.should_parse_by_mimetype('text/csv'))
        self.assertFalse(self.parser.should_parse_by_mimetype('application/vs-excel'))

    def test_should_parse_by_filename(self):
        "Responds to proper extensions."
        self.assertTrue(self.parser.should_parse_by_filename('myfile/test.tsv'))
        self.assertFalse(self.parser.should_parse_by_filename('myfile/test.csv'))
        self.assertFalse(self.parser.should_parse_by_filename('myfile/test.xls'))

    def test_can_parse(self):
        "Test determining which files are parsable."
        for filename in self.tsv_filenames:
            with self.file_handle(filename) as fh:
                self.assertTrue(self.parser.can_parse(fh))

        for filename in self.csv_filenames + self.excel_filenames:
            with self.file_handle(filename) as fh:
                self.assertFalse(self.parser.can_parse(fh))

    def test_parse(self):
        "Test parsing TSV files."
        filename = 'tsv/imf_disb_repay.tsv'
        with self.file_handle(filename) as fh:
            first = list(self.parser.parse(fh).next())
            self.assertEquals(first, self.first_line)
