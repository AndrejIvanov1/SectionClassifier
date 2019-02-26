"""
Usage:
	author_fasttext_test.py --train_file <train_file> --test_file <test_file> --model_file <model_file> [--epoch <epoch>] [--dim <dim>] [--lr <lr>] [--n_gram <n_gram>] [--loss <loss>] [--retrain]

Options:
	--train_file <train_file> Path to the train dataset
	--test_file <test_file> Path to test dataset
	--model_file <model_file> Where to save the model
	--epoch <epoch> Number of training epochs [10]
	--dim <dim> Size of words vectors [300]
	--lr <lr> Learning rate [0.25]
	--n_gram <n_gram> Max lenght of word n-grams [3]
	--loss <loss> Loss function [softmax]
	--retrain Do not restore previous model
"""
import fasttext
import os
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from docopt import docopt
import matplotlib.pyplot as plt	
import time

model_path = "model.bin"
train_path = "data/fasttext/train.txt"
test_path = "data/fasttext/test.txt"
small_dataset_path = "data/fasttext/small_dataset.txt"

def plot_class_distribution(labels, title='Class distributution'):
	plt.hist(labels, color='blue', edgecolor='black', align='mid')
	plt.title(title)
	plt.show()


def read_label(line):
	label = line.split(' ')[0]
	label = label[9:]
	return int(label)

def read_text(line):
	return line.split(' ', 1)[1]

def read_texts(lines):
	return list(map(lambda line: read_text(line), lines))

def read_labels(lines):
	return list(map(lambda line: read_label(line), lines))

if __name__ == "__main__":
	arguments = docopt(__doc__)
	print("Arguments: ", arguments)

	train_path = arguments["<train_file>"]
	test_path = arguments["<test_file>"]
	model_path = arguments["<model_file>"]

	epoch = int(arguments["<epoch>"])
	dim = int(arguments["<dim>"])
	lr = float(arguments["<lr>"])
	n_gram = int(arguments["<n_gram>"])
	loss = arguments["<loss>"]
	retrain = arguments["--retrain"]

	print(epoch, dim, lr, n_gram, loss, retrain)

	if not retrain and os.path.exists(model_path + ".bin"):
		print("Restoring previous model from {}".format(model_path + ".bin"))
		start_time = time.time()
		clf = fasttext.load_model(model_path + ".bin")
		print("Restored in {} seconds. ".format(time.time() - start_time))
		#print("Labels", clf.labels)
	else:
		print("Training model ...")
		start_time = time.time()
		clf = fasttext.supervised(train_path, model_path,
								  epoch=epoch, 
								  dim=dim, 
								  lr=lr,
								  loss=loss,
								  word_ngrams=n_gram,
								  bucket=200000)
		print("Trained in {} seconds. ".format(time.time() - start_time))

	#print(clf.__dict__)
	

	lines = open(test_path, 'r').read().strip().split('\n')
	true_labels = read_labels(lines)

	#plot_class_distribution(true_labels)

	lines = read_texts(lines)
	start_time = time.time()
	predicted_labels = clf.predict(lines)
	print("Predicted in {} seconds. ".format(time.time() - start_time))

	predicted_labels = [int(x[0]) for x in predicted_labels]
	
	print(true_labels[:2])
	print(predicted_labels[:2])

	print(len(true_labels), len(predicted_labels))
	assert len(true_labels) == len(predicted_labels)

	print(classification_report(true_labels, predicted_labels, labels=list(set(true_labels))))
	#print(confusion_matrix(true_labels, predicted_labels))
	print(accuracy_score(true_labels, predicted_labels))