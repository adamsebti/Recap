#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk import tokenize
import sys
import operator
import codecs
import math
import unicodedata

prepositions = ["aboard", "about", "above","across","after","against","along","amid","among","anti","around","as","at",
"before","behind","below", "would", "could", "beneath","beside","besides","between","beyond","but","by","concerning",
"considering","despite","down","during","except","excepting","excluding","following","for","from","in",
"inside","into","like","near","of","off","on","onto","outside","over","past","per","plus",
"regarding","since","than","through","towards","under","do", "underneath","unlike","versus","via","with",
"within","without", "a", "and", "the", "have", "to", "was", "were", "be", "an", "no"]

pronouns = [
"all","another","any","anybody","anyone","anything","both","each","eachother","either","everybody","everyone",
"everything","few","he","her","hersherself","him","himself","his","I","it","its","itself","many","me","mine","more",
"most","much","my","myself","neither","noone","nobody","none","nothing","one","oneanother","other",
"others","our","ourselves","several","she","some","somebody","someone","something","that","their",
"theirs","them","themselves","these","they","this","those","us","we","what","whatever","which",
"whichever","who","whoever","whom","whomever","whose","you","your","yours","yourself","yourselves", "has"]

conjunctions = ["and", "or", "but" ,"nor", "so", "for", "yet"
,"after","although","as","because","before","even","provided","since","so","that","though","until",
"unless","when","whenever","wherever","whether","while", 
"who","whom","what","whose","which","when","where","why","how","is", "said"]

not_words = prepositions + pronouns + conjunctions


def summarize(article, lines=3):
	"""Returns a summary of the article
	article: string"""
	wordDict = dict()
	# create an array with all the words in the article
	words = split_line(get_sentences(article))
	# create a dictionary with the frequency of each word
	for word in words:
		if word[0] == '"' or word[0] == "'":
			word = word[1:]
		elif word[-1] in [',', '.', ';', ':']:
			word = word[:-1]
		num = int(math.floor(len(word) * .75))
		subWord = word[:num]
		if subWord in wordDict:
			wordDict[subWord] = wordDict[subWord] + 1
		elif word in wordDict:
			wordDict[word] = wordDict[word] + 1
		else:
			wordDict[word] = 1
	wordDict = sorted(wordDict.items(), key=operator.itemgetter(1))

	# generate top keywords
	keywords = ""
	keywordsdict = sorted(wordDict, key=lambda x: x[1])[-5:][::-1]
	for keyword in keywordsdict:
		keywords += keyword[0].title() + ", "
	keywords = keywords[:-2]

	# generate summary
	sentences = get_sentences(article)
	if lines > len(sentences): #in case article length < requested summary length
		lines = len(sentences)
	sentenceVal = []
	for idx,sentence in enumerate(sentences):
		val = get_sentence_val(sentence, wordDict)
		sentenceVal.append(val)
	indicies = max_indexes(sentenceVal, lines)
	summary = ""
	for i in indicies:					
		summary += sentences[i] + ". ± "
	return [summary, keywords]

def split_line(text):
	"""Returns an array of words in an article
	text: string"""
	result = []
	# for each sentence in the article:
	for words in text:
		# for each word in the sentence
		for word in words.split(' '):
			word = word.lower()
			if word not in not_words and len(word) > 2:
				if word[-2:] == "'s":
					word = word[:-2]
				if word[-1:] == "s":
					word = word[:-1]
				result.append(word)
	return result

	return result

def get_sentences(paragraph):
	sentences = tokenize.sent_tokenize(paragraph)
	for idx,sentence in enumerate(sentences):
		sentences[idx] = sentence[:-1]
	return sentences

def get_sentence_val(sentence, freq):
	val = 0
	words = split_words(sentence)
	for word in words:
		if word in freq:
			val += freq[word]
		else:
			val += 1
	return val

def split_words(text):
	"""Returns an array of words in a sentence
	text: string"""
	result = []
	# for each word in the line:
	for word in text.split(' '):
		word = word.lower()
		if word not in not_words and len(word) > 2:
			if word[-2:] == "'s":
				word = word[:-2]
			if word[-1:] == "s":
				word = word[:-1]
			result.append(word)
	return result

def max_index(array):
	"""Returns index of maximum element in
	array"""
	index = 0
	max = -sys.maxsize
	for idx,val in enumerate(array):
		if val > max:
			index = idx
			max = val
	return index

def max_indexes(array, n):
	indicies = [0]
	array[0] = -sys.maxsize
	while n > 1:
		index = max_index(array)
		indicies += [index]
		n -= 1
		array[index] = -sys.maxsize
	indicies.sort()
	return indicies

if __name__ == '__main__':

	article = sys.argv[1]
	article = article.replace('\n', ' ')
	article = article.replace('\r', '')

	sentences = int(sys.argv[2])


	summary = summarize(article , sentences)

	#summary
	print(summary[0])
	#reduced by
	print(int((len(summary[0])/len(article))*100))
	#top keywords
	print(summary[1])



