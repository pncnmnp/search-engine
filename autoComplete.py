from time import time

class TrieNode:
	def __init__(self):
		self.children = [None]*26
		self.endOfWord = False

class Trie:
	def __init__(self):
		self.root = TrieNode()

	def insert(self, val):
		move = self.root

		for level in val:
			index = ord(level) - ord('a')

			if not move.children[index]:
				move.children[index] = TrieNode()
			move = move.children[index]
		
		move.endOfWord = True

	def search(self, val):
		move = self.root

		for level in val:
			index = ord(level) - ord('a')

			if not move.children[index]:
				return False
			move = move.children[index]
		return move != None	and move.endOfWord

	def display(self, move, val, level):
		if move != None and move.endOfWord:
			print(''.join(val))

		for i in range(26):
			if move.children[i]:
				val[level] = chr(i + 97)
				self.display(move.children[i], val, level+1)
			else:
				val[level] = ''

	def autoSearch(self, move, key, search, level):
		if (''.join(search)).startswith(key):
			self.display(move, search, level)

		elif key not in ''.join(search):
			for i in range(26):
				if move.children[i]:
					search[level] = chr(i + 97)
					self.autoSearch(move.children[i], key, search, level+1)
				else:
					search[level] = ''

def getWords(filename, words):
	with open(filename) as file:
		for word in file.read().split():
			val = ''.join([i for i in word if i.isalpha()])
			words.append(str(val.lower()))

def search(words):
	trie = Trie()
	
	for val in words:
		trie.insert(val)
	
	val = ['']*200

	while(True):
		print('CTRL C to exit !')
		try:
			find = input('Enter the word to be autocompleted: ').lower()
			# Time = time()
			trie.autoSearch(trie.root, find, val, 0)
			# print('About ' + str(time()-Time) + ' seconds')
			print()
		except KeyboardInterrupt:
			print()
			return

def main():
	words = []
	file = './DataFiles/harrypotter.txt'
	getWords(file, words)
	search(words)

if __name__ == '__main__':
	main()