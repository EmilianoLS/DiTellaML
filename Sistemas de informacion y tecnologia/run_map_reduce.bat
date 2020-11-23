pip install nltk
python -m nltk.downloader punkt stopwords
python mapper.py reviews/* | python reducer.py
