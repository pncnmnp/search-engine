from sys import exit
import os
from time import time

def editDistance(str1, str2):
	m = len(str1)
	n = len(str2)
	dp = [[0 for i in range(n+1)] for j in range(m+1)]

	for i in range(m+1):
		for j in range(n+1):
			if i is 0:
				dp[i][j] = j
			elif j is 0:
				dp[i][j] = i
			elif str1[i-1] == str2[j-1]:
				dp[i][j] = dp[i-1][j-1]
			else:
				dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])
	
	return (dp[m][n])

def printDP(m, n, dp):
	for i in range(m):
		for j in range(n):
			print(dp[i][j], end=' ')
		print()	

def getWords(filename, words):
	os.chdir('../')
	with open(filename) as file:
		for word in file.read().split():
			val = ''.join([i for i in word if i.isalpha()])
			words.append(str(val.lower()))
	os.chdir('website/')

def spellChecker(words, searchQuery):
	search = searchQuery
	possibleOutcomes = []

	if search in words:
		print('Dictionary Word !!')
		# exit(0)

	Time = time()
		
	for word in words:
		# Ldist stands for levenshtein distance
		Ldist = editDistance(search, word)
		if(Ldist <= 2):
			word = word + str(Ldist)
			possibleOutcomes.append(word)

	# print('Did You mean: ', end=' ')
	for index in range(1,3):
		for word in possibleOutcomes:
			if(int(word[-1:]) == index):
				return word[:-1]
				# print('About ' + str(time() - Time)[0:4] + ' seconds')
				# exit(0)

def main(searchQuery):
	filename = './DataFiles/harrypotter.txt'
	words = []
	getWords(filename, words)
	dym = spellChecker(words, searchQuery)
	return dym

if __name__ == '__main__':
	main()