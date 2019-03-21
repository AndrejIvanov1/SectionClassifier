from load_data import get_section_names, load_dataset, abbreviate_labels
from sklearn.model_selection import train_test_split
import os


train_dataset_path = os.path.join("data", "fasttext_format","train.txt")
test_dataset_path = os.path.join("data", "fasttext_format","test.txt")

if __name__ == "__main__":
	data, labels = load_dataset(get_section_names(), max_samples=-1)
	X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True)

	assert len(X_train) == len(y_train)
	assert len(X_test) == len(y_test)

	with open(train_dataset_path, 'w+', encoding='UTF-8') as f:
		for i in range(len(X_train)):
			f.write("__label__{} {}\n".format(y_train[i], X_train[i]))

	with open(test_dataset_path, 'w+', encoding='UTF-8') as f:
		for i in range(len(X_test)):
			f.write("__label__{} {}\n".format(y_test[i], X_test[i])) 