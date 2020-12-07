import argparse
import pandas as pd
import numpy as np 
import math
import operator
from itertools import islice



#Characterize your topics by computing the 10 words in each category with the highest tf-idf scores
#(to compute the inverse document frequency, use all 2,000 posts that you originally collected)

# python3 compute_tfidf.py ./../data/processed/politics.tsv ./../data/processed/conservative.tsv ./../data/processed/politics_hot_1000_titles.json ./../data/processed/conservative_hot_1000_titles.json

def calc_tfidf(num_topic_appearance, num_topics, num_topics_term):
	#number of times the term appears in titles assigned to the topic * log([# of topics]/[# of topics that term is used in])
	return num_topic_appearance * math.log(num_topics/num_topics_term)

parser = argparse.ArgumentParser()

parser.add_argument('politics_data', type=argparse.FileType('r'), help='politics dataset')
parser.add_argument('conservative_data', type=argparse.FileType('r'), help='conservative dataset')
parser.add_argument('politics_all', type=argparse.FileType('r'), help='all politics data')#politics_hot_1000_titles.json
parser.add_argument('conservative_all', type=argparse.FileType('r'), help='all conservative data')#conservative_hot_1000_titles.json

args = parser.parse_args()

politics_df = pd.read_csv(args.politics_data, sep='\t', names=["topic", "title"])
conservative_df = pd.read_csv(args.conservative_data, sep='\t') #Already has headers
politics_data_all = pd.read_json(args.politics_all, lines=True)
conservative_data_all = pd.read_json(args.conservative_all, lines=True)

temp_politics_df = politics_df['title'].drop_duplicates(keep=False)
temp_conservative_df = conservative_df['title'].drop_duplicates(keep=False)

politics_df_all = pd.concat([politics_data_all, temp_politics_df]).drop_duplicates()
conservative_df_all = pd.concat([conservative_data_all, temp_conservative_df]).drop_duplicates()
total_df = pd.concat([politics_df_all, conservative_df_all])
total_df['topic'] = 'other'
total_df.columns = ["title", "topic"]
	
topic_list = ["election challenge", "election general", "pandemic", "domestic policy/politics", "foreign relations"]
politics_dict = {"election challenge": {}, "election general": {}, "pandemic": {}, "domestic policy/politics": {}, "foreign relations": {}}
conservative_dict = {"election challenge": {}, "election general": {}, "pandemic": {}, "domestic policy/politics": {}, "foreign relations": {}}

punctuation = ["(", ")", "[", "]", ",", "-", ".", "?", "!", ":", ";", "#", "&", "\\", "`"]

num_topics_term_dict = {} #Number of topics that term is used in (max value should be 5, check with "print(set(num_topics_term.values()))"" ) 

tfidf_dict = {"election challenge": {}, "election general": {}, "pandemic": {}, "domestic policy/politics": {}, "foreign relations": {}}

other_dict = {}

for index, row in total_df.iterrows():
	row['title'] = row['title'].lower().translate({ord(p): " " for p in punctuation})
	for word in row.title.split():
		if word not in num_topics_term_dict:
			num_topics_term_dict[word] = 0
		if word not in other_dict:
			other_dict[word] = 1
		else:
			other_dict[word] += 1

#Filter politics annotated dataset
for index, row in politics_df.iterrows():
	row['title'] = row['title'].lower().translate({ord(p): " " for p in punctuation})
	for word in row.title.split():
		if word not in num_topics_term_dict:
			num_topics_term_dict[word] = 0
		if word not in politics_dict[row.topic]:
			politics_dict[row.topic][word] = 1
		else:
			politics_dict[row.topic][word] += 1

#Filter conservative annotated dataset
for index, row in conservative_df.iterrows():
	row['title'] = row['title'].lower().translate({ord(p): " " for p in punctuation})
	for word in row.title.split():
		if word not in num_topics_term_dict:
			num_topics_term_dict[word] = 0
		if word not in conservative_dict[row.topic]:
			conservative_dict[row.topic][word] = 1
		else:
			conservative_dict[row.topic][word] += 1

#Compute number of topics the term appears in 
for word in num_topics_term_dict:
	for x in topic_list:
		if word in politics_dict[x] or word in conservative_dict[x]:
			num_topics_term_dict[word] += 1
for word in num_topics_term_dict:
	if word in other_dict:
		num_topics_term_dict[word] += 1

term_appearance_sum = {}

for topic in politics_dict:
	for word in politics_dict[topic]:
		if word not in term_appearance_sum:
			term_appearance_sum[word] = 1
		else:
			term_appearance_sum[word] += 1
for topic in conservative_dict:
	for word in conservative_dict[topic]:
		if word not in term_appearance_sum:
			term_appearance_sum[word] = 1
		else:
			term_appearance_sum[word] += 1

for topic in topic_list:
	num_topics = 6
	for word in politics_dict[topic]:
		num_topic_appearance = term_appearance_sum[word] #number of time the term appears in titles assigned to the topic
		num_topics_term = num_topics_term_dict[word] #number of topics that term is used in
		tfidf_dict[topic][word] = calc_tfidf(num_topic_appearance, num_topics, num_topics_term)
	for word in conservative_dict[topic]:
		num_topic_appearance = term_appearance_sum[word]
		num_topics_term = num_topics_term_dict[word]
		tfidf_dict[topic][word] = calc_tfidf(num_topic_appearance, num_topics, num_topics_term)


def take(n, iterable):
    #"Return first n items of the iterable as a list"
    return list(islice(iterable, n))

for x in tfidf_dict:
	tfidf_dict[x] = dict(sorted(tfidf_dict[x].items(), key=lambda item: item[1], reverse=True))
	# print(list(tfidf_dict[x])[:10])

print()
print("TF-IDF RESULTS")
for x in tfidf_dict:
	print(take(10, tfidf_dict[x].items()))

print()

def topic_count(dataframe):
	results = {"election challenge": 0, "election general": 0, "pandemic": 0 , "domestic policy/politics": 0, "foreign relations": 0}
	for index, row in dataframe.iterrows():
		results[row['topic']] += 1
	return results

print("POLITICS TOPIC COUNT")
print(topic_count(politics_df))
print()
print("CONSERVATIVE TOPIC COUNT")
print(topic_count(conservative_df))
print()
		

























