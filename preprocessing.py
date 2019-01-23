from nltk.tokenize import word_tokenize

"""
	Parameters: data - list of paragraphs as strings
	Returns: list of paragraphs as lists of words
"""
def split_words(data):
	return list(map(lambda paragraph: word_tokenize(paragraph), data))

