import argparse
import math
from pathlib import Path
import pandas
import pyarrow
import pyarrow.parquet as pq
import requests
from unidecode import unidecode
from nltk import word_tokenize
from nltk.corpus import stopwords
#stopword list to use
spanish_stopwords = stopwords.words('spanish')


buffer = []
tfs = {}
term_buckets = {}
term_categories = {}

totals = {  'positive':{'MLA1039': {'zhiyun':6,
                                    'zocalo':25},
                        'MLA5725':{ 'hola':7,
                                    'zocalo':5}},
            'negative':{'MLA1051': {'zona':40,
                                    'hola':5,
                                    'zocalo': 1},
                        'MLA1039':{'zocalo':6},
                        'MLA555':{'hola':5}}}

for bucket, bucket_totals in totals.items():
    tfs[bucket] = {}
    for category, category_totals in bucket_totals.items():
        tfs[bucket][category] = {}
        for term, frequency in category_totals.items():
            tfs[bucket][category][term] = frequency / sum(category_totals.values())

            if term not in term_buckets:
                term_buckets[term] = set()
            term_buckets[term].add(bucket)

            if term not in term_categories:
                term_categories[term] = set()
            term_categories[term].add(category)

print('TFS')

print(set(tfs['negative'].keys()))

#print(term_categories)
#total_occurences_positive = 0
#total_occurences_negative = 0
#for elemento in buffer:

#    if elemento[2] == 'positive':
#
#        total_occurences_positive += 1
#    else:
#        total_occurences_negative += 1
#
#    totals.update('bucket':)
#print(buffer[0][0])