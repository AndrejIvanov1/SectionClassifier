import fasttext
import os
from sklearn.metrics import confusion_matrix, accuracy_score

model_path = "model.bin"
train_path = "data/fasttext/train.txt"
test_path = "data/fasttext/test.txt"
small_dataset_path = "data/fasttext/small_dataset.txt"

def read_labels(lines):
	return list(map(lambda line: line[9], lines))

if __name__ == "__main__":

	if os.path.exists(model_path):
		clf = fasttext.load_model(model_path)
	else:
		clf = fasttext.supervised(train_path, 'model')
	

	lines = open(test_path, 'r', encoding='UTF-8').read().strip().split('\n')
	true_labels = read_labels(lines)
	
	lines = list(map(lambda line: line[9:], lines))
	predicted_labels = clf.predict(lines)
	print(predicted_labels)
	predicted_labels = [x[0] for x in predicted_labels]
	#rint(predicted_labels)
	predicted_labels = read_labels(predicted_labels)

	print(len(true_labels), len(predicted_labels))
	assert len(true_labels) == len(predicted_labels)

	print(confusion_matrix(true_labels, predicted_labels))
	print(accuracy_score(true_labels, predicted_labels))