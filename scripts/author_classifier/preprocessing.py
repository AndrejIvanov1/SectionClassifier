from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

"""
	Parameters: text - list of paragraphs as strings
	Returns: list of paragraphs as lists of words
"""
stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))

def _split_words(text):
	return word_tokenize(text)

def _lowercase(text):
	return list(map(lambda word: word.lower(), text))

def _remove_stopwords(text):
	return list(filter(lambda word: word not in stop_words, text))

def _stem_word(word):
	try:
		return stemmer.stem(word)
	except:
		return word


def _stem(text):
	return list(map(lambda word: _stem_word(word), text))

def preprocess(text, split_words=True, lowercase=False, remove_stopwords=False, do_stem=False):
	if split_words:
		text = _split_words(text)
	if lowercase:
		text = _lowercase(text)
	if remove_stopwords:
		text = _remove_stopwords(text)
	if do_stem:
		text = _stem(text)

	text = ' '.join(text)
	return text
""" 
def remove_punctuation(text):
	return list(map(lambda paragraph: list(filter())
"""


