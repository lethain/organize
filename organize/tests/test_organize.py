"""
Test using the ``organize.organize`` function,
which is the primary interface for using the module.
"""
from organize import organize
from organize.tests import OrganizeTestCase


class TestOrganize(OrganizeTestCase):
    "Test organize function."

    def test_csv(self):
        "Test parsing a CSV."
        filename = 'csv/worldbank_preamble.csv'
        first_line = [
            (u'Country', u'Belarus'), (u'Year', u'2000'),
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

        with self.file_handle(filename) as fh:
            lines = organize(fh)
            first = list(lines.next())
            self.assertEquals(first, first_line)

    def test_tsv(self):
        "Test parsing a TSV."
        filename = 'tsv/imf_disb_repay.tsv'
        first_line = [
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
        with self.file_handle(filename) as fh:
            lines = organize(fh)
            first = list(lines.next())
            self.assertEquals(first, first_line)

    def test_to_dict(self):
        "Test transforming into dicts as described in README."
        filename = 'tsv/imf_disb_repay.tsv'
        first_dict = {
            u'PRGT Interest Paid': u'0',
            u'GRA Disbursements': u'2,765,465,000',
            u'GRA Charges Paid': u'584,358,716',
            u'Total Charges and Interest': u'584,358,716',
            u'PRGT Disbursements': u'63,266,571',
            u'Total Repayments': u'5,559,606,670',
            u'Year': u'2014',
            u'PRGT Repayments': u'132,553,847',
            u'GRA Repurchases': u'5,427,052,823',
            u'Total Disbursements': u'2,828,731,571',
        }

        with self.file_handle(filename) as fh:
            lines = organize(fh)
            first = dict(list(lines.next()))
            self.assertEquals(first, first_dict)
