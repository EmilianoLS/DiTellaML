import argparse
import math
from pathlib import Path
import pandas
import pyarrow
import pyarrow.parquet as pq
import requests


table2 = pq.read_table(r'C:\Users\Emi\Desktop\MLA57250.parquet')
new_df = table2.to_pandas()

print(new_df.Dis.value_counts())
