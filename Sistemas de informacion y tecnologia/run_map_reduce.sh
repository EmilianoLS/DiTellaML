pip install nltk
python -m nltk.downloader punkt stopwords
python utdtmeli/mapper.py utdtmeli/reviews/* | python utdtmeli/reducer.py
