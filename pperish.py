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

# from nltk.book import * 

# Some globals
DIR = "/Users/angelaambroz/python/_resources/nltk/"
PROFS = [{'name': 'Rohini', 'homepage': 'http://www.hks.harvard.edu/fs/rpande/research.html', 'top': 'http://www.hks.harvard.edu/fs/rpande/'}, 
{'name': 'Esther', 'homepage': 'http://economics.mit.edu/faculty/eduflo/papers', 'top': 'http://economics.mit.edu'}, 
{'name': 'Asim', 'homepage': 'http://www.hks.harvard.edu/fs/akhwaja/', 'top': 'http://www.hks.harvard.edu/fs/akhwaja/'},
{'name': 'Rema', 'homepage': 'http://scholar.harvard.edu/remahanna/published-and-forthcoming', 'top': ''},
{'name': 'Mike', 'homepage': 'http://scholar.harvard.edu/michael-callen/current-publications', 'top': ''}
]

QUICKRUN = 1 # switch to 0 to download all
if QUICKRUN==1:
	n = 11
	m = 2
elif QUICKRUN==0:
	n = None
	m = None


# Get URLs for all papers
def getPapers(url):
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	papers = []
	for link in soup.find_all('a'):
		if link.get("href") and "pdf" in link.get("href"):
			papers.append(link.get("href"))
		if link.get("href") and "files" in link.get("href"):
			papers.append(link.get("href"))	
	return papers


# Scrape text from all papers
def stripText(papers, top):
	text = []
	for url in papers:
		if url[0:4]!="http":
			url = top + url

		print url
		
		try:
			urllib2.urlopen(url)
			urllib.urlretrieve(url, DIR + "paper.pdf")
			
			os.system("pdf2txt.py -o paper.txt -t text paper.pdf")
			raw = open(DIR + "paper.txt").read()
			text.append(raw)

		except:
			print "Problem with opening the URL."

	if os.path.isfile(DIR + "paper.pdf"):
		os.remove(DIR + "paper.pdf") 
	if os.path.isfile(DIR + "paper.txt"):
		os.remove(DIR + "paper.txt")
	return text

# Create corpus

# for pi in PROFS:
# 	print "Now doing: " + pi['name']
# 	print "Getting " + pi['name'] + "'s papers..."
# 	papers = getPapers(pi['homepage'])
# 	print "Scraping the text from " + pi['name'] + "'s papers..."
# 	name = pi['name']
# 	file = open(DIR + "corpi/" + pi['name'] + ".txt", "w")
# 	strings = stripText(papers, pi['top'])
# 	print strings[0:5]

# 	if strings=="":
# 		file.close()
# 	else:
# 		file.write(str(strings))
# 		file.close()

# NLTK: Cleaning + Analysis
# Ch. 3 of the NLTK O'Reilly book is proving helpful here


# Fun: p.125, NLTK book
def Przm(word):
	regexp = r'^[AEIOUaeiou]+|[AEIOUaeiou]+$|[^AEIOUaeiou]'
	pieces = re.findall(regexp, word)
	return ''.join(pieces)


def Analysis(name):
	raw = open(DIR + "corpi/" + name + ".txt", 'rU').read()

	tokens = nltk.word_tokenize(raw)
	tokens = [w.lower() for w in tokens]

	print nltk.tokenwrap(Przm(w) for w in tokens[:20])

	# Cleaning that cleans nothing (something wrong w my RE?)
	tokens = [re.sub(r'^([\"\n]|[\\x[a-z0-9]])+[a-zA-z]$', '', w) for w in tokens]

	vocab = sorted(set(tokens))
	print len(vocab)

	sents = nltk.sent_tokenize(raw)
	random_sentence = random.choice(sents)
	print random_sentence

	# fdist = nltk.FreqDist(ch.lower() for ch in raw if ch.isalpha())

	text = nltk.Text(tokens)
	print text[1020:1060]

	fdist = nltk.FreqDist(tokens)
	fdist = sorted(fdist.items(), key=operator.itemgetter(1))
	# print fdist[-50:]

	# long_words = [w for w in tokens if len(w) > 15]

	ings = {}

	# for word in tokens:
	# 	elif word.endswith("ing"):
	# 		if word not in ings.keys():
	# 			ings[word] = 1
	# 		elif word in ings.keys():
	# 			ings[word] += 1
	# ings = sorted(ings.items(), key=operator.itemgetter(1))


	# pp = pprint.PrettyPrinter(indent=4)
	# pp.pprint(fdist[-10:])






# Demo
Analysis("Asim")


# Analyzing all profs

# for pi in PROFS:
# 	if pi['name']!="Mike":
# 		print "Now analyzing: " + pi['name']
# 		Analysis(pi['name'])

