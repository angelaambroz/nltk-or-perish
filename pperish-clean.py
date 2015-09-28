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

"""
Scraping the data.
"""

# Some globals
DIR = os.getcwd()

PROFS = [{'name': 'Rohini', 'homepage': 'http://www.hks.harvard.edu/fs/rpande/research.html', 'top': 'http://www.hks.harvard.edu/fs/rpande/'}, 
{'name': 'Asim', 'homepage': 'http://www.hks.harvard.edu/fs/akhwaja/', 'top': 'http://www.hks.harvard.edu/fs/akhwaja/'},
{'name': 'Rema', 'homepage': 'http://scholar.harvard.edu/remahanna/published-and-forthcoming', 'top': ''},
{'name': 'Mike', 'homepage': 'http://scholar.harvard.edu/michael-callen/current-publications', 'top': ''},
{'name': 'Abhijit', 'homepage': 'http://economics.mit.edu/faculty/banerjee/papers', 'top': 'http://economics.mit.edu'},
{'name': 'Esther', 'homepage': 'http://economics.mit.edu/faculty/eduflo/papers', 'top': 'http://economics.mit.edu'}
]


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

for pi in PROFS:
	if not os.path.isfile(DIR + "corpi/" + pi["name"] + ".txt"):
		print "Now doing: " + pi['name']
		print "Getting " + pi['name'] + "'s papers..."
		papers = getPapers(pi['homepage'])
		print "Scraping the text from " + pi['name'] + "'s papers..."
		name = pi['name']
		file = open(DIR + "corpi/" + pi['name'] + ".txt", "w")
		strings = stripText(papers, pi['top'])
		print strings[0:5]

		if strings=="":
			file.close()
		else:
			file.write(str(strings))
			file.close()

