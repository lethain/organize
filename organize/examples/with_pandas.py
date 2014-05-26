from organize import organize
import pandas as pd

filename = 'your_file.csv'
with open(filename, 'r') as fin:
    df = pd.DataFrame.from_records(organize(fin, filename=filename))
    print df
