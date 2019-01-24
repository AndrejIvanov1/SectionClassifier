from load_data import load_dataset, get_section_names
from preprocessing import split_words, remove_stopwords, lowercase
if __name__ == "__main__":
	data, labels = load_dataset(get_section_names(), max_samples=4)
	data = split_words(data)
	data = lowercase(data)
	data = remove_stopwords(data)
	print(data[0])
	print(data[10])
