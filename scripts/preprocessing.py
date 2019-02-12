from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

"""
	Parameters: data - list of paragraphs as strings
	Returns: list of paragraphs as lists of words
"""
def _split_words(data):
	return list(map(lambda paragraph: word_tokenize(paragraph), data))


def _lowercase(data):
	return list(map(lambda paragraph: list(map(lambda word: word.lower(), paragraph)), data))


def _remove_stopwords(data):
	stop_words = set(stopwords.words("english"))
	return list(map(lambda paragraph: list(filter(lambda word: word not in stop_words, paragraph)), data))


def _stem(data):
	stemmer = PorterStemmer()
	return list(map(lambda paragraph: list(map(lambda word: stemmer.stem(word), paragraph)), data))


def preprocess(data, split_words=False, lowercase=False, remove_stopwords=False, stem=False):
	if split_words:
		data = _split_words(data)
	if lowercase:
		data = _lowercase(data)
	if remove_stopwords:
		data = _remove_stopwords(data)
	if stem:
		data = _stem(data)

	return data
""" 
def remove_punctuation(data):
	return list(map(lambda paragraph: list(filter())
"""


