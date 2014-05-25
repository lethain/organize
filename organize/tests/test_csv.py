"Test CSV parsing."
import unittest
import organize.csv_parser


class TestCSVParser(unittest.TestCase):
    "Test CSV."
    def setUp(self):
        "Test CSV parser."
        self.parser = organize.csv_parser.CSVParser()

    def test_should_parse_by_mimetype(self):
        "Responds to proper mimetype."
        self.assertTrue(self.parser.should_parse_by_mimetype('text/csv'))
        self.assertFalse(self.parser.should_parse_by_mimetype('application/vs-excel'))
        self.assertFalse(self.parser.should_parse_by_mimetype('text/tsv'))

    def test_should_parse_by_filename(self):
        "Responds to proper extensions."
        self.assertTrue(self.parser.should_parse_by_filename('test.csv'))
        self.assertTrue(self.parser.should_parse_by_filename('myfile/test.csv'))
        self.assertFalse(self.parser.should_parse_by_filename('myfile/test.xls'))
        self.assertFalse(self.parser.should_parse_by_filename('myfile/test.tsv'))



if __name__ == '__main__':
    unittest.main()
