import scrapy
import csv
import os
import re
from nltk.stem.wordnet import WordNetLemmatizer
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class Indexing:
	def __init__(self):
		self.links = []
		self.stopWords = []
		self.toRefine = []
		self.invertedIndex = {}

	def getLinks(self):
		os.chdir('./getLinks')
		for word in open('links.jl'):
			self.links.append((word).replace("\n",""))

	def getStopWords(self):
		os.chdir("../")
		for word in open('./DataFiles/stopwords.txt'):
			self.stopWords.append((word).replace("\n", ""))

	def checkStopWords(self):
		newSearchList = []
		for word in self.toRefine:
			if word not in self.stopWords:
				newSearchList.append(word)
		self.toRefine = newSearchList		

	def checkLemma(self):
		lemma = WordNetLemmatizer()
		for word in self.toRefine:
			lemmatized = lemma.lemmatize(word)
			self.toRefine[self.toRefine.index(word)] = lemmatized

	def indexRefinedWords(self, link):
		for word in self.toRefine:
			self.invertedIndex.setdefault(word, {})

			# Finding the frequency of each word with the corresponding link
			# Storing in a nested dictionary
			if link not in self.invertedIndex[word]:
				(self.invertedIndex[word])[link] = 1
			elif link in self.invertedIndex[word]:
				(self.invertedIndex[word])[link] += 1					

	def refineWords(self, link, toRefine):
		self.toRefine = toRefine
		self.checkStopWords()
		self.checkLemma()
		self.indexRefinedWords(link)

	def makeCSV(self):
		with open('data.csv', 'w') as file:
			writer = csv.writer(file)
			for key in self.invertedIndex:
				for item in self.invertedIndex[key]:
					writer.writerow([key, item, self.invertedIndex[key][item]])
		
class Scraping(scrapy.Spider):
	name = "indexing"
	indexing = Indexing()
	indexing.getStopWords()
	indexing.getLinks()
	start_urls = indexing.links

	# This is required for spider_closed to work
	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	# This is only suitable for wikipedia links
	# Do change the tags for appropriate scraping
	def parse(self, response):
		for div in response.css('div.mw-parser-output'):
			for text in div.css('p ::text'):
				refining = text.extract().lower()
				refining = re.compile('\w+').findall(refining);
				self.indexing.refineWords(response.url, refining)

	# Gets computed after all the scraping has been done
	def spider_closed(self, spider):
		self.indexing.makeCSV()