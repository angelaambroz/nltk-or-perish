#!/usr/local/bin/python 

import urllib2
import urllib
import os
import re
import random
import pprint
import operator
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords


"""
NLTK analysis.
"""

# Some globals
DIR = os.getcwd()
STOP = stopwords.words('english')


# NLTK: Cleaning + Analysis
# Ch. 3, NLTK book

# Fun: p.125, NLTK book
def Przm(word):
	regexp = r'^[AEIOUaeiou]+|[AEIOUaeiou]+$|[^AEIOUaeiou]'
	pieces = re.findall(regexp, word)
	return ''.join(pieces)

def Tokenize(rawfile):
	words = nltk.word_tokenize(rawfile)
	words = [w.lower() for w in words]

	# Cleaning that cleans nothing (something wrong w my RE?)
	# words = [re.sub(r'^([\"\n]|[\\x[a-z0-9]])+[a-zA-z]$', '', w) for w in words]

	sents = nltk.sent_tokenize(rawfile)

	fulltext = nltk.Text(words)

	return words, sents, fulltext

def Characteristics(words):
	vocab = sorted(set(words))
	bigram_fd = nltk.FreqDist(nltk.bigrams(words))

	return len(vocab), bigram_fd


def randomSentence(sents):
	random_sentence = random.choice(sents)
	return random_sentence

def FreqDists(words):
	fdist = nltk.FreqDist(words)
	# fdist = sorted(fdist.items(), key=operator.itemgetter(1))
	top_words = [i for i in fdist.most_common(50) if i not in STOP]

	cfd = nltk.ConditionalFreqDist(top_words)

	return fdist, cfd, top_words


# A bunch of print statements?
def Analysis(corpus):
	raw = open(corpus, 'rU').read()

	words, sents, text = Tokenize(raw)

	random_sentence = randomSentence(sents)

	fdist, cfd, top_words = FreqDists(words)

	print nltk.tokenwrap(Przm(w) for w in words[:20])
	print fdist
	cfd.tabulate()


	# print text[1020:1060]
	# print [i for i in fdist.most_common(50) if i not in STOP]

	# long_words = [w for w in tokens if len(w) > 15]

	# ings = {}

	# for word in tokens:
	# 	elif word.endswith("ing"):
	# 		if word not in ings.keys():
	# 			ings[word] = 1
	# 		elif word in ings.keys():
	# 			ings[word] += 1
	# ings = sorted(ings.items(), key=operator.itemgetter(1))



# Demo
Analysis(DIR + "/corpi/Asim.txt")


# Analyzing all corpi

# for corpus in os.listdir(DIR + "corpi/"):
# 	print "Now analyzing: " + corpus
# 	Analysis(corpus)


