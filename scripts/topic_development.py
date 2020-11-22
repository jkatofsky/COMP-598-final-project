import argparse
import json
import requests
import os
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
  
lemmatizer = WordNetLemmatizer()

parser = argparse.ArgumentParser()
parser.add_argument('data', type=argparse.FileType('r'), help="json file with reddit posts")
args = parser.parse_args()

stop_words = stopwords.words('english')
punctuation = string.punctuation + "’" + "‘" + "“" + "”" 

json_data = args.data.read()
title_list = []

for x in json_data.splitlines():
	title_list.append(json.loads(x)['data']['title'])

filtered_titles = []

for x in title_list:
	word_tokens = word_tokenize(x)
	title_filter = [lemmatizer.lemmatize(w).lower() for w in word_tokens if not w in stop_words and not w in punctuation]
	filtered_titles.append(title_filter)

top_freq = {}

for title in filtered_titles:
	for word in title:
		if word not in top_freq:
			top_freq[word] = 1
		else:
			top_freq[word] += 1

sorted_dict = dict(sorted(top_freq.items(), key=lambda item: item[1], reverse=True))
print(sorted_dict)