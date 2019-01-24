from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
"""
	Parameters: data - list of paragraphs as strings
	Returns: list of paragraphs as lists of words
"""
def split_words(data):
	return list(map(lambda paragraph: word_tokenize(paragraph), data))


def lowercase(data):
	return list(map(lambda paragraph: list(map(lambda word: word.lower(), paragraph)), data))


def remove_stopwords(data):
	stop_words = set(stopwords.words("english"))
	return list(map(lambda paragraph: list(filter(lambda word: word not in stop_words, paragraph)), data))


""" 
def remove_punctuation(data):
	return list(map(lambda paragraph: list(filter())
"""


