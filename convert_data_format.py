from load_data import load_dataset, get_section_names
from sklearn.model_selection import train_test_split
import os

train_dataset_path = os.path.join("data", "fasttext", "train.txt")
test_dataset_path = os.path.join("data", "fasttext", "test.txt")

def _save_dataset(data, labels, path):
	with open(path, 'w', encoding='UTF-8') as f:
		for i in range(len(data)):
			f.write("__label__{} {}\n".format(labels[i], data[i]))


"""
	Converts the data to a format the fastText library can work with
"""
if __name__ == "__main__":
	data, labels = load_dataset(get_section_names(), max_samples=-1)
	assert len(data) == len(labels)

	X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.25, shuffle=True)

	assert len(X_train) == len(y_train)
	assert len(X_test) == len(y_test)

	#_save_dataset(X_train, y_train, train_dataset_path)
	_save_dataset(X_test, y_test, test_dataset_path)