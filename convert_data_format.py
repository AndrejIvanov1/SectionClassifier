"""
Usage:
	convert_data_format.py --train_file <train_file> --test_file <test_file> [--randomized]

Options:
	--train_file <train_file> Path to the train dataset
	--test_file <test_file> Path to test dataset
	--randomized Save dataset with randomized(incorrect) labels
"""
from docopt import docopt
from load_data import load_dataset, get_section_names
from sklearn.model_selection import train_test_split
from random import randint
from fasttext_test import plot_class_distribution
import os

train_dataset_path = os.path.join("data", "fasttext", "train.txt")
test_dataset_path = os.path.join("data", "fasttext", "test.txt")

def _save_dataset(data, labels, path, randomized=False):
	with open(path, 'w', encoding='UTF-8') as f:
		for i in range(len(data)):
			label = randint(1, 10) if randomized else labels[i]
			f.write("__label__{} {}".format(label, data[i]))


"""
	Converts the data to a format the fastText library can work with
"""
if __name__ == "__main__":
	arguments = docopt(__doc__)
	train_dataset_path = arguments["<train_file>"]
	test_dataset_path = arguments["<test_file>"]
	randomized = arguments["--randomized"]

	data, labels = load_dataset(get_section_names(), max_samples=-1)
	assert len(data) == len(labels)

	X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.25, shuffle=True)

	assert len(X_train) == len(y_train)
	assert len(X_test) == len(y_test)

	plot_class_distribution(y_train, title='Train class distribution')
	plot_class_distribution(y_test, title='Test class distribution')

	_save_dataset(X_train, y_train, train_dataset_path, randomized=randomized)
	_save_dataset(X_test, y_test, test_dataset_path, randomized=randomized)