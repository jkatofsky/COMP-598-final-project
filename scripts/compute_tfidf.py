import argparse
import pandas as pd
import numpy as np 
import math

#Characterize your topics by computing the 10 words in each category with the highest tf-idf scores
#(to compute the inverse document frequency, use all 2,000 posts that you originally collected)

def calc_tfidf(num_topic_appearance, num_topics, num_topics_term):
	#number of times the term appears in titles assigned to the topic * log([# of topics]/[# of topics that term is used in])
	return num_topic_appearance * math.log(num_topics/num_topics_term)

parser = argparse.ArgumentParser()

parser.add_argument('politics_data', type=argparse.FileType('r'), help='politics dataset')
#Annotations: election challenge, election general, pandemic, domestic policy/politics, foreign relations
parser.add_argument('politics_all', type=argparse.FileType('r'), help='all politics data')#politics_hot_1000_titles.json

# parser.add_argument('conservative_data', type=argparse.FileType('r'), help='conservative dataset')
# parser.add_argument('conservative_all', type=argparse.FileType('r'), help='all conservative data')#conservative_hot_1000_titles.json

args = parser.parse_args()

politics_df = pd.read_csv(args.politics_data, sep='\t', names=["topic", "title"])
politics_data_all = args.politics_all.read()

politics_dict = {"election challenge": {}, "election general": {}, "pandemic": {}, "domestic policy/politics": {}, "foreign relations": {}}
# punctuation = ["(", ")", "[", "]", ",", "-", ".", "?", "!", ":", ";", "#", "&"]
punctuation = ["(", ")", "[", "]", ",", "-", ".", "?", "!", ":", ";", "#", "&", "'", "\"", "`"]
# row['dialog'] = row['dialog'].lower().translate({ord(p): " " for p in punctuation})
#Replaces punctuation with whitespace


num_topics_term_dict = {} # Number of topics that term is used in (max value should be 5, check with "print(set(num_topics_term.values()))"" ) 
tfidf_dict = {"election challenge": {}, "election general": {}, "pandemic": {}, "domestic policy/politics": {}, "foreign relations": {}}

for index, row in politics_df.iterrows():
	#Filtering (probably needs to be more thorough)
	row['title'] = row['title'].lower().translate({ord(p): " " for p in punctuation})
	#not getting rid of '\\u2019s'
	for word in row.title.split():


		if word not in num_topics_term_dict:
			num_topics_term_dict[word] = 0


		if word not in politics_dict[row.topic]:
			politics_dict[row.topic][word] = 1
		else:
			politics_dict[row.topic][word] += 1

for word in num_topics_term_dict:
	for x in politics_dict:
		if word in politics_dict[x]:
			num_topics_term_dict[word] += 1

for topic in politics_dict:
	for word in politics_dict[topic]:
		num_topic_appearance = politics_dict[topic][word]
		num_topics = len(politics_dict)
		num_topics_term = num_topics_term_dict[word]

		tfidf_dict[topic][word] = calc_tfidf(num_topic_appearance, num_topics, num_topics_term)

for x in tfidf_dict:
	tfidf_dict[x] = dict(sorted(tfidf_dict[x].items(), key=lambda item: item[1], reverse=True))
	print(list(tfidf_dict[x])[:10])

# print(tfidf_dict)




		
		

























