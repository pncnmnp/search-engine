import csv
import re
import didYouMean
import autoComplete
from sys import exit
import os
from nltk.stem.wordnet import WordNetLemmatizer

class Retrival:
	def __init__(self):
		self.searchList = []
		self.originalQuery = ''
		self.stopWords = []
		self.links = {}
		self.flink = [] # final links
		self.dym = [] # Did You Mean

	def getStopWords(self):
		os.chdir('../')
		# print(os.getcwd())
		for word in open('./DataFiles/stopwords.txt'):
			self.stopWords.append((word).replace("\n",""))
		os.chdir('website/')

	def checkLemma(self):
		lemma = WordNetLemmatizer()
		for word in self.searchList:
			lemmatized = lemma.lemmatize(word)
			self.searchList[self.searchList.index(word)] = lemmatized

	def checkStopWords(self):
		newSearchList = []
		for word in self.searchList:
			if word not in self.stopWords:
				newSearchList.append(word)
		self.searchList = newSearchList

	def checkCSV(self):
		os.chdir('../')
		csv_file = csv.reader(open('./getLinks/data.csv', 'r'), delimiter=",")
		
		# mergeLinks = [[] for i in range(len(self.searchList))]
		# unionLinks = []

		for row in csv_file:
			for searchWord in self.searchList:
				if searchWord in row[0]:

					# mergeLinks[self.searchList.index(searchWord)].append(str(row[1]))
					# if len(self.searchList) == 1:
					# 	unionLinks = mergeLinks
					# else:
					# 	unionLinks = list(set.intersection(*map(set, mergeLinks)))

					row_link = str(row[1])
					row_rank = row[2]
					if row_link in self.links: #and row_link in unionLinks:
						self.links[row_link] += int(row_rank)
					else: #row_link in unionLinks:
						self.links[row_link] = int(row_rank)
		os.chdir('website/')

	def results(self):
		links = sorted(self.links.items(), key=lambda kv: kv[1])[::-1]
		links_upto = 10
		current_link_no = 0
		if links == []:
			print('No Results Found')
			for word in self.searchList:
				self.dym.append(didYouMean.main(word))
			return

		for link in links:
			print(link[0], link[1])
			self.flink.append(link[0])
			current_link_no += 1
			if(current_link_no == links_upto):
				break


	def searchRequest(self, searchq):
		self.getStopWords()
		# self.searchList = re.compile('\w+').findall(((str(input('Search : '))).lower()))
		self.searchList = re.compile('\w+').findall((searchq).lower())
		self.originalQuery = ' '.join(self.searchList)
		self.checkStopWords()
		self.checkLemma()
		self.checkCSV()
		self.results()

if __name__ == '__main__':
	searchq = ''
	search = Retrival()	
	search.searchRequest(searchq)