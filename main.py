from load_data import load_dataset, get_section_names
from preprocessing import preprocess
if __name__ == "__main__":
	data, labels = load_dataset(get_section_names(), max_samples=4)

	data = preprocess(data, split_words=True, lowercase=True, remove_stopwords=True, stem=True)
	
	print(data[0])
	print(data[10])
