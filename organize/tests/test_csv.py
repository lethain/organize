"Test CSV parsing."
import unittest
import organize.csv_parser
import os.path


class TestCSVParser(unittest.TestCase):
    "Test CSV."
    def setUp(self):
        "Test CSV parser."
        self.parser = organize.csv_parser.CSVParser()
        self.data_path = os.path.join(os.path.dirname(__file__), 'data')
        self.csv_filenames = ['csv/Baby_Names__Beginning_2007.csv',  'csv/worldbank.csv']
        self.tsv_filenames = ['tsv/imf_disb_repay.tsv']

    def file_handle(self, filename):
        "Create file handle for a data file."
        path = os.path.join(self.data_path, filename)
        return open(path, 'r')

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

    def test_can_parse(self):
        "Test determining which files are parsable."
        for filename in self.csv_filenames:
            with self.file_handle(filename) as fh:
                self.assertTrue(self.parser.can_parse(fh))

        for filename in self.tsv_filenames:
            with self.file_handle(filename) as fh:
                self.assertFalse(self.parser.can_parse(fh))


if __name__ == '__main__':
    unittest.main()
