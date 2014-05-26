"Init file for tests directory."
import unittest
import os.path


class OrganizeTestCase(unittest.TestCase):
    """
    ``unittest.TestCase`` subclass with a few extra
    utility methods to simplify testing.
    """
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    csv_filenames = ['csv/Baby_Names__Beginning_2007.csv',  'csv/worldbank.csv']
    tsv_filenames = ['tsv/imf_disb_repay.tsv']
    excel_filenames = ['excel/irrat_exu_robert_shiller.xlsx', 'excel/simple.xlsx', 'excel/simple_old.xls']

    def file_handle(self, filename):
        "Create file handle for a data file."
        path = os.path.join(self.data_path, filename)
        return open(path, 'r')
