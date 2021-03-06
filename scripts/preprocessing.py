from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

"""
	Parameters: text - list of paragraphs as strings
	Returns: list of paragraphs as lists of words
"""
def _split_words(text):
	return word_tokenize(text)

def _lowercase(text):
	return list(map(lambda word: word.lower(), text))

def _remove_stopwords(text):
	stop_words = set(stopwords.words("english"))
	return list(filter(lambda word: word not in stop_words, text))

def _stem(text):
	stemmer = PorterStemmer()
	return list(map(lambda word: stemmer.stem(word), text))

def preprocess(text, split_words=True, lowercase=False, remove_stopwords=False, stem=False):
	if split_words:
		text = _split_words(text)
	if lowercase:
		text = _lowercase(text)
	if remove_stopwords:
		text = _remove_stopwords(text)
	if stem:
		text = _stem(text)
		
	return text
""" 
def remove_punctuation(text):
	return list(map(lambda paragraph: list(filter())
"""


