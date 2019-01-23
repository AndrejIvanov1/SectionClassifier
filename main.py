from load_data import load_dataset, get_section_names

if __name__ == "__main__":
	data, labels = load_dataset(get_section_names())
	