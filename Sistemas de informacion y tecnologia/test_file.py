import argparse
import math
from pathlib import Path
import pandas
import pyarrow
import pyarrow.parquet as pq
import requests
from unidecode import unidecode


string = 'HolA t#ód?o b+íen'

print(string.lower())
print(unidecode(string))
