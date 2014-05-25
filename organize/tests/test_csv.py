"Test CSV parsing."
from itertools import islice
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
        self.worldbank_first_line = [(u'Country', u'Belarus'), (u'Year', u'2000'),
                                     (u'CO2 emissions (metric tons per capita)', u'5.91'),
                                     (u'Electric power consumption (kWh per capita)', u'2988.71'),
                                     (u'Energy use (kg of oil equivalent per capita)', u'2459.67'),
                                     (u'Fertility rate, total (births per woman)', u'1.29'),
                                     (u'GNI per capita, Atlas method (current US$)', u'1.38E+03'), 
                                     (u'Internet users (per 1,000 people)', u'18.69'),
                                     (u'Life expectancy at birth, total (years)', u'68.01'),
                                     (u'Military expenditure (% of GDP)', u'1.26'),
                                     (u'Population, total', u'1.00E+07'),
                                     (u'Prevalence of HIV, total (% of population ages 15-49)', u''),
        ]

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

    def test_parse(self):
        "Test parsing CSV files."
        filename = 'csv/worldbank.csv'
        with self.file_handle(filename) as fh:
            first = list(self.parser.parse(fh).next())
            self.assertEquals(first, self.worldbank_first_line)

    def test_parse_despite_empty_lines(self):
        "Test parsing CSV files with empty lines scattered about."
        filename = 'csv/worldbank_whitespace.csv'
        with self.file_handle(filename) as fh:
            lines = self.parser.parse(fh)
            first = list(lines.next())
            self.assertEquals(first, self.worldbank_first_line)
            self.assertEquals(3, len(list(lines)))

    def test_parse_despite_preamble(self):
        "Test parsing CSV files with empty lines scattered about and a preamble."
        filename = 'csv/worldbank_preamble.csv'
        with self.file_handle(filename) as fh:
            lines = self.parser.parse(fh)
            first = list(lines.next())
            self.assertEquals(first, self.worldbank_first_line)
            self.assertEquals(3, len(list(lines)))


if __name__ == '__main__':
    unittest.main()
