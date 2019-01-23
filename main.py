from load_data import load_dataset, get_section_names
from preprocessing import split_words
if __name__ == "__main__":
	data, labels = load_dataset(get_section_names(), max_samples=4)
	data = split_words(data)
	print(data[0])
